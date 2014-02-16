import os
import sys
import time
import socket
import urllib2
import tempfile
from functools import wraps
from StringIO import StringIO
import urlparse
from flask import Flask, send_file, request, abort
from utils import jsonify

# TODO remove this and do use client launcher
this_dir = os.path.dirname(os.path.realpath(__file__))
core_dir = os.path.join(os.path.dirname(this_dir), 'core')
sys.path.insert(1, core_dir)
# leave this though
from module import use_module, path, packaging

# flask app
app = Flask(__name__, static_folder='public', static_url_path='')

STORE_URL = 'http://localhost:8889'

def allowed_file(filename, exts):
    return '.' in filename and filename.rsplit('.', 1)[1] in exts
IMAGE_EXTS = ['png', 'jpg', 'jpeg', 'gif', 'bmp']

# fix for index page
@app.route('/')
def index():
    return app.send_static_file('index.html')

# move in module ?
@app.route('/api/rooms')
def api_rooms():
    return app.send_static_file('rooms.json')

@app.route('/api/modules')
def api_modules():
    return jsonify(packaging.get_installed_modules(detailed=True))

@app.route('/api/modules/<module_name>/info')
def api_module_info(module_name):
    try:
        return jsonify(use_module(module_name, False).info)
    except (TypeError, socket.error) as e:
        import logging
        log = logging.getLogger()
        log.exception(e)
        abort(404)

def route_with_module_posted(url):
    def decorator(f):
        @wraps(f)
        def view(*args, **kwargs):
            try:
                module_name = request.form['name']
            except KeyError:
                abort(400)
            else:
                return f(module_name, *args, **kwargs)
        return app.add_url_rule(url, view_func=view, methods=['POST'])
    return decorator

@route_with_module_posted('/api/modules/install')
def api_install_module(module_name):
    try:
        io = StringIO()
        zipfile = urllib2.urlopen(urlparse.urljoin(STORE_URL,
            '/api/available_modules/%s/download' % module_name))
        io.write(zipfile.read())
        packaging.install_from_zip(io)
    except urllib2.HTTPError:
        abort(404)
    except IOError:
        abort(403)
    return jsonify({ 'success': False })

@route_with_module_posted('/api/modules/uninstall/<instance_id>')
def api_uninstall_module(module_name, instance_id):
    print 'Stopping instance %s of module %s' % (instance_id, module_name)
    pass #instance.stop(module_name, instance_id)

@app.route('/api/modules/upload', methods=['POST'])
def api_upload_module():
    return_data = { 'success': False }
    file_ = request.files['file']
    if not file_:
        abort(400)
    if not allowed_file(file_.filename, ['zip']):
        abort(403)

    # all is good, let's go !
    _, filename = tempfile.mkstemp()
    file_.save(filename)
    try:
        packaging.install_from_zip(filename)
    except (IOError, ValueError):
        abort(403)
    else:
        return_data['success'] = True
    finally:
        os.remove(filename)
    return jsonify(return_data)

@app.route('/api/modules/<module_name>/public/<rest>')
def api_module_public(module_name, rest):
    rest = rest.lstrip('.') # for security reasons
    try:
        module_config = packaging.get_config(module_name)
    except IOError:
        abort(404)

    # send the requested file
    module_dir = path.module_directory(module_name)
    module_public_dir = module_config.get('public_directory', 'public')
    requested_file = os.path.join(module_dir, module_public_dir, rest)
    if os.path.exists(requested_file):
        return send_file(requested_file)
    else:
        abort(404)

# Proxies for store service
# TODO get these dynamically
if __name__ == '__main__':
    from functools import partial
    from utils import proxy
    with app.app_context():
        store_proxy = partial(proxy, STORE_URL)
        store_proxy('/api/available_modules')
        store_proxy('/api/available_modules/<module_name>/public/<rest>')
        store_proxy('/api/available_modules/rate', methods=['POST'])

# used for samples
import random

def brightness_statuses():
    r = lambda: int(random.random()*10)
    return [ { 'name': 'b1', 'time': time.time(), 'attrs': { 'brightness': r() } },
             { 'name': 'b2', 'time': time.time(), 'attrs': { 'brightness': r() } },
             { 'name': 'b3', 'time': time.time(), 'attrs': { 'brightness': r() } }, ]

def temperature_statuses():
    r = lambda: int(random.random()*40)
    return [ { 'name': 't1', 'time': time.time(), 'attrs': { 'temperature': r() } },
             { 'name': 't2', 'time': time.time(), 'attrs': { 'temperature': r() } },
             { 'name': 't3', 'time': time.time(), 'attrs': { 'temperature': r() } }, ]

@app.route('/api/modules/<module_name>/instances/status')
def api_module_instances_statuses(module_name):
    if packaging.is_installed(module_name):
        mod = use_module(module_name)
        if mod:
            fields = {}
            for f in mod.info['fields']:
                if 'readable' in f and f['readable']:
                    field_fn = getattr(mod, f['name'])
                    value = field_fn()
                    if value is not None:
                        fields += [{'name': f['name'],
                            'time': value[0],
                            'value': value[1]}]
            return jsonify(fields)
        else:
            abort(404)
    else:
        abort(404)

    if module_name == 'temperature':
        return jsonify(temperature_statuses())
    elif module_name == 'brightness':
        return jsonify(brightness_statuses())

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug='--debug' in sys.argv, port=8888)
