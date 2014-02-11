import os
import sys
import zipfile
import tempfile
from flask import (Flask, send_file, abort)
from app import jsonify
from utils import crossdomain

# TODO remove this and do use client launcher
this_dir = os.path.dirname(os.path.realpath(__file__))
core_dir = os.path.join(os.path.dirname(this_dir), 'core')
sys.path.insert(1, core_dir)
# leave this though
import catalog

app = Flask(__name__)

@app.route('/api/available_modules')
@crossdomain(origin='*')
def api_available_modules():
    return jsonify(catalog.get_available_modules(detailed=True))

@app.route('/api/available_modules/<module_name>/icon')
@crossdomain(origin='*')
def api_available_module_icon(module_name):
    module_name = module_name.lstrip('.') # for security reasons
    dir_ = catalog.AVAILABLE_DIRECTORY
    module_zipfile = os.path.join(dir_, module_name + '.zip')
    with zipfile.ZipFile(module_zipfile) as zf:
        try:
            print 'ok'
            module_conf_filename = os.path.join(module_name, catalog.CONFIG_FILE)
            with zf.open(module_conf_filename) as module_conf_zf:
                module_conf = json.load(module_conf_zf)
            print 'ok'
            public_dir = module_conf.get('public_dir', 'public')
            icon_file = os.path.join(module_name, public_dir, 'icon.png')
            with zf.open(icon_file) as icon_zf:
                print 'ok'
                try:
                    res = None
                    _, icon_filename = tempfile.mkstemp()
                    with open(icon_filename, 'w') as fp:
                        fp.write(icon_zf.read())
                    print 'ok'
                    res = send_file(icon_filename)
                finally:
                    os.remove(icon_filename)
                    if res:
                        return res
                    else:
                        abort(404)
        except (KeyError, IOError):
            abort(404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug='--debug' in sys.argv, port=8889)
