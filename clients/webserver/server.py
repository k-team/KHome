import os
import sys
import json
import time
import tempfile
from flask import (Flask, Response, send_file, request, abort,
        jsonify as _jsonify)

# remove this and do in client launcher
this_dir = os.path.dirname(os.path.realpath(__file__))
core_dir = os.path.join(os.path.dirname(os.path.dirname(this_dir)), 'core')
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

@app.route('/api/rooms')
def api_rooms():
    return app.send_static_file('rooms.json')

@app.route('/api/modules')
def api_modules():
    return jsonify(catalog.get_installed_modules(detailed=True))

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

@app.route('/api/modules/<module_name>/icon')
def api_module_icon(module_name):
    icon_path = catalog.get_config(module_name).get('icon')

    # default module icon
    if icon_path is None:
        return app.send_static_file('img/module.png')

    # specified icon: either relative to module directory (eg. starting with
    # "."), or given by an absolute path
    if icon_path.startswith('.'):
        module_directory = catalog.get_directory(module_name)
        full_icon_path = os.path.join(module_directory, icon_path)
    else:
        full_icon_path = icon_path

    # final return
    if os.path.exists(full_icon_path):
        return send_file(full_icon_path)
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
