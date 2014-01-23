import os
import sys
import json
import time
import tempfile
from flask import (Flask, Response, send_file, request, jsonify as _jsonify)

# remove this and do in client launcher
this_dir = os.path.dirname(os.path.realpath(__file__))
core_dir = os.path.join(os.path.dirname(os.path.dirname(this_dir)), 'core')
sys.path.insert(1, core_dir)
# leave this though
from catalog import (install_from_zip, get_installed_modules)

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

# fix for index page
@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/rooms')
def rooms():
    return app.send_static_file('rooms.json')

@app.route('/api/modules')
def modules():
    return jsonify(get_installed_modules())

@app.route('/api/modules/install', methods=['POST'])
def upload_module():
    return_data = { 'success': False }
    file_ = request.files['file']
    if file_:
        if not allowed_file(file_.filename, ['zip']):
            return_data['message'] = 'File format not allowed'
        else:
            _, filename = tempfile.mkstemp()
            file_.save(filename)
            try:
                install_from_zip(filename)
            except (IOError, ValueError) as e:
                return_data['message'] = str(e)
            else:
                return_data['success'] = True
            finally:
                os.remove(filename)
    else:
        return_data['message'] = 'No file uploaded'
    return jsonify(return_data)

# used for samples
import random

def brightness_statuses():
    r = lambda: int(random.random()*10)
    return [ { 'name': 'b1', 'data': { 'time': time.time(), 'value': r() } },
            { 'name': 'b2', 'data': { 'time': time.time(), 'value': r() } },
            { 'name': 'b3', 'data': { 'time': time.time(), 'value': r() } }, ]

def temperature_statuses():
    r = lambda: int(random.random()*40)
    return [ { 'name': 't1', 'data': { 'time': time.time(), 'value': r() } },
            { 'name': 't2', 'data': { 'time': time.time(), 'value': r() } },
            { 'name': 't3', 'data': { 'time': time.time(), 'value': r() } }, ]

@app.route('/api/modules/<module_name>/instances/status')
def module_instances_statuses(module_name):
    if module_name == 'temperature':
        return jsonify(temperature_statuses())
    elif module_name == 'brightness':
        return jsonify(brightness_statuses())

if __name__ == '__main__':
    app.run(debug='--debug' in sys.argv or conf.get('debug', False),
            port=int(conf.get('port', 8888)))
