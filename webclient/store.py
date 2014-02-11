import os
import sys
import json
import zipfile
import tempfile
from flask import (Flask, request, send_file, abort)
from werkzeug.utils import secure_filename
from app import jsonify
from utils import crossdomain

# TODO remove this and do use client launcher
this_dir = os.path.dirname(os.path.realpath(__file__))
core_dir = os.path.join(os.path.dirname(this_dir), 'core')
sys.path.insert(1, core_dir)
# leave this though
import catalog

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/api/available_modules', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def api_available_modules():
    return jsonify(catalog.get_available_modules(detailed=True))

@app.route('/api/available_modules/<module_name>/public/<rest>', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def api_available_module_public(module_name, rest):
    # security check
    module_name, rest = map(secure_filename, (module_name, rest))
    if not allowed_file(rest):
        abort(403)

    # get zip file from catalog
    dir_ = catalog.AVAILABLE_DIRECTORY
    module_zipfile = os.path.join(dir_, module_name + '.zip')
    with zipfile.ZipFile(module_zipfile) as zf:
        try:
            module_conf_filename = os.path.join(module_name, catalog.CONFIG_FILE)
            with zf.open(module_conf_filename) as module_conf_zf:
                module_conf = json.load(module_conf_zf)
            public_dir = module_conf.get('public_dir', 'public')
            requested_file = os.path.join(module_name, public_dir, rest)
            with zf.open(requested_file) as requested_zf:
                try:
                    res = None
                    _, fname = tempfile.mkstemp()
                    with open(fname, 'w') as fp:
                        fp.write(requested_zf.read())
                    res = send_file(fname)
                finally:
                    os.remove(fname)
                    if res:
                        return res
                    else:
                        abort(404)
        except (KeyError, IOError):
            abort(404)

@app.route('/api/available_modules/<module_name>/rate', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def api_available_module(module_name):
    try:
        value = request.form['value']
        print value
    except KeyError:
        abort(404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug='--debug' in sys.argv, port=8889)
