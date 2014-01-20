import os
import sys

# remove this and do in module launcher
this_dir = os.path.dirname(os.path.realpath(__file__))
core_dir = os.path.join(os.path.dirname(os.path.dirname(this_dir)), 'core')
sys.path.insert(1, core_dir)

# used for bootstrapping
import random

import json
from modules import (get_socket as get_module_socket,
        get_all as get_all_modules)
from flask import (Flask, Response, send_file, jsonify as _jsonify)

def jsonify(obj):
    """
    Updated jsonify, adding list support.
    """
    if isinstance(obj, list):
        return Response(obj, mimetype='application/json')
    return _jsonify(obj)

# configuration
with open('client.json', 'r') as fp:
    conf = json.load(fp)

# flask app
app = Flask(__name__,
        static_folder=conf.get('static_directory', 'static'),
        static_url_path='')

# fix for index page
@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/rooms')
def rooms():
    return app.send_static_file('rooms.json')

@app.route('/api/modules')
def modules():
    return jsonify(json.dumps(get_all_modules()))

@app.route('/api/modules/<module_instance>/status')
def module_status(module_instance):
    if module_instance == 't_module_1':
        temp_status = { 'temperature': random.random()*40 }
        return jsonify(temp_status)

if __name__ == '__main__':
    app.run(debug='--debug' in sys.argv or conf.get('debug', False),
            port=int(conf.get('port', 8888)))
