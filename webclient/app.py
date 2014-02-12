import os
import sys
import time
import socket
import tempfile
import urlparse
import requests
from flask import Flask, send_file, request, abort, make_response
from utils import jsonify

# TODO remove this and do use client launcher
this_dir = os.path.dirname(os.path.realpath(__file__))
core_dir = os.path.join(os.path.dirname(this_dir), 'core')
sys.path.insert(1, core_dir)
# leave this though
import catalog
from module import use_module

# flask app
app = Flask(__name__, static_folder='public', static_url_path='')

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

@app.route('/api/modules/<module_name>/fields')
def api_module_configure(module_name):
    try:
        return jsonify(use_module(module_name).fields)
    except socket.error:
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
    module_dir = catalog.get_module_directory(module_name)
    module_public_dir = module_config.get('public_directory', 'public')
    requested_file = os.path.join(module_dir, module_public_dir, rest)
    if os.path.exists(requested_file):
        return send_file(requested_file)
    else:
        abort(404)

def store_proxy(url):
    """
    Generates an app route pointing to the same relative url as the specified
    store url. Doesn't return anything, only add the route.
    The generated route acts as a proxy for the store server.
    """
    store_url = 'http://localhost:8889'
    view_name = url.strip('/').replace('/<>', '_')
    def view(*args, **kwargs):
        request_func = getattr(requests, request.method.lower())
        view_url = urlparse.urljoin(store_url, request.path)
        r = request_func(view_url, headers=request.headers, data=request.data)
        resp = make_response(r.content)
        resp.headers['Content-type'] = r.headers['Content-type']
        resp.status_code = r.status_code
        return resp
    app.add_url_rule(url, view_name, view_func=view)

# Proxies for store service
# TODO get these dynamically
if __name__ == '__main__':
    store_proxy('/api/available_modules')
    store_proxy('/api/available_modules/<module_name>/public/<rest>')
    store_proxy('/api/available_modules/<module_name>/rate')

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
    app.run(host='0.0.0.0', debug='--debug' in sys.argv, port=8888)
