import os
import sys
import json
import time
import zipfile
import tempfile
from flask import (Flask, Response, send_file, request, abort,
        jsonify as _jsonify)

# remove this and do in client launcher
this_dir = os.path.dirname(os.path.realpath(__file__))
core_dir = os.path.join(os.path.dirname(this_dir), 'core')
sys.path.insert(1, core_dir)
# leave this though
import catalog

def jsonify(obj):
    """
    Updated jsonify, adding list support.
    """
    if isinstance(obj, list):
        return Response(json.dumps(obj), mimetype='application/json')
    return _jsonify(obj)

# configuration
with open('client.json', 'r') as fp:
    conf = json.load(fp)

# flask app
app = Flask(__name__,
        static_folder=conf.get('static_directory', 'static'),
        static_url_path='')

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
    return jsonify(catalog.get_installed_modules(detailed=True))

@app.route('/api/available_modules')
def api_available_modules():
    return jsonify(catalog.get_available_modules(detailed=True))

@app.route('/api/available_modules/<module_name>/icon')
def api_available_module_icon(module_name):
    module_name = module_name.lstrip('.') # for security reasons
    dir_ = catalog.AVAILABLE_DIRECTORY
    module_zipfile = os.path.join(dir_, module_name + '.zip')
    with zipfile.ZipFile(module_zipfile) as zf:
        try:
            module_conf_filename = os.path.join(module_name, catalog.CONFIG_FILE)
            with zf.open(module_conf_filename) as module_conf_zf:
                module_conf = json.load(module_conf_zf)
            public_dir = module_conf.get('public_dir', 'public')
            icon_file = os.path.join(module_name, public_dir, 'icon.png')
            with zf.open(icon_file) as icon_zf:
                try:
                    res = None
                    _, icon_filename = tempfile.mkstemp()
                    with open(icon_filename, 'w') as fp:
                        fp.write(icon_zf.read())
                    res = send_file(icon_filename)
                finally:
                    os.remove(icon_filename)
                    if res:
                        return res
                    else:
                        abort(404)
        except (KeyError, IOError):
            abort(404)

@app.route('/api/modules/install', methods=['POST'])
def api_upload_module():
    return_data = { 'success': False }
    file_ = request.files['file']
    if file_:
        if not allowed_file(file_.filename, ['zip']):
            return_data['message'] = 'File format not allowed'
        else:
            _, filename = tempfile.mkstemp()
            file_.save(filename)
            try:
                catalog.install_from_zip(filename)
            except (IOError, ValueError) as e:
                return_data['message'] = str(e)
            else:
                return_data['success'] = True
            finally:
                os.remove(filename)
    else:
        return_data['message'] = 'No file uploaded'
    return jsonify(return_data)

@app.route('/api/modules/<module_name>/public/<rest>')
def api_module_public(module_name, rest):
    rest = rest.lstrip('.') # for security reasons
    try:
        module_config = catalog.get_config(module_name)
    except IOError:
        abort(404)

    # send the requested file
    module_dir = catalog.get_directory(module_name)
    module_public_dir = module_config.get('public_directory', 'public')
    requested_file = os.path.join(module_dir, module_public_dir, rest)
    if os.path.exists(requested_file):
        return send_file(requested_file)
    else:
        abort(404)

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
    if module_name == 'temperature':
        return jsonify(temperature_statuses())
    elif module_name == 'brightness':
        return jsonify(brightness_statuses())

if __name__ == '__main__':
    app.run(debug='--debug' in sys.argv or conf.get('debug', False),
            port=int(conf.get('port', 8888)))
