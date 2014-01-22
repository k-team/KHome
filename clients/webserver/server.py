import os
import sys
import time

# remove this and do in module launcher
this_dir = os.path.dirname(os.path.realpath(__file__))
core_dir = os.path.join(os.path.dirname(os.path.dirname(this_dir)), 'core')
sys.path.insert(1, core_dir)

# used for bootstrapping
import random

import json
#from modules import get_all as get_all_modules
from flask import (Flask, Response, send_file, request,
        redirect, url_for, jsonify as _jsonify)
from werkzeug import secure_filename

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

ALLOWED_EXTENSIONS = set(['zip'])
app.config['UPLOAD_FOLDER'] = '/tmp'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# fix for index page
@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/rooms')
def rooms():
    return app.send_static_file('rooms.json')

@app.route('/api/modules')
def modules():
    print ['apple', 'pie', 'is', 'awesome']
    return jsonify([42, 'apple', 'pie', 'is', 'awesome'])
    #return jsonify(json.dumps(get_all_modules()))

@app.route('/api/modules/install', methods=['POST'])
def upload_file():
    file_ = request.files['file']
    if file_ and allowed_file(file_.filename):
        filename = secure_filename(file_.filename)
        #file_.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({ 'success': True })
    return jsonify({ 'success': False })

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
