import os
import sys
import json
import zipfile
import tempfile
from werkzeug.utils import secure_filename
from werkzeug.contrib.cache import SimpleCache
from flask import (Flask, request, send_file, send_from_directory, abort)
from flask_peewee.db import Database
from peewee import *
from utils import jsonify, cached

# TODO remove this and do use client launcher
this_dir = os.path.dirname(os.path.realpath(__file__))
core_dir = os.path.join(os.path.dirname(this_dir), 'core')
sys.path.insert(1, core_dir)
# leave this though
import catalog
from module import path

app = Flask(__name__, static_folder=path.availables_directory())
cache = SimpleCache()

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# configure our database
app.config['DATABASE'] = {
        'name': os.path.join(this_dir, 'store.db'),
        'engine': 'peewee.SqliteDatabase',
        }

# instantiate the db wrapper
db = Database(app)

# write the models

class Rating(db.Model):
    module = CharField()
    value = IntegerField()

    @classmethod
    def average(cls, module_name):
        return cls.get(cls.module == module_name).select(
                fn.Avg(cls.value).alias('value'))[0].value

# finish setting up database
if __name__ == '__main__':
    Rating.create_table(fail_silently=True)

@cached
@app.route('/api/available_modules')
def api_available_modules():
    available_modules = catalog.get_available_modules(detailed=True)
    for av in available_modules:
        try:
            av['rating'] = Rating.average(av['id'])
        except Rating.DoesNotExist:
            pass
    return jsonify(available_modules)

@cached
@app.route('/api/available_modules/<module_name>/public/<rest>')
def api_available_module_public(module_name, rest):
    # security check
    module_name, rest = map(secure_filename, (module_name, rest))
    if not allowed_file(rest):
        abort(403)

    # get zip file from catalog
    with zipfile.ZipFile(catalog.get_zipfile(module_name)) as zf:
        try:
            module_conf_filename = os.path.join(module_name, path.CONFIG_FILE)
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

@cached
@app.route('/api/available_modules/<module_name>/download')
def api_available_module_download(module_name):
    module_zipfile = catalog.get_zipfile(module_name).split(os.path.sep)[-1]
    return send_from_directory(app.static_folder, module_zipfile,
            as_attachment=True)

@cached
@app.route('/api/available_modules/rate', methods=['POST'])
def api_available_module_set_rate():
    """
    TODO: api key for rating
    """
    # validate module name
    try:
        print request.form
        module_name = request.form['name']
    except KeyError:
        abort(400)

    # check that the module is indeed available
    if not catalog.is_available(module_name):
        abort(404)

    # save the new rating
    try:
        value = int(request.form['value'])
        Rating.create(module=module_name, value=value)
        return jsonify({ 'success': True })
    except (ValueError, KeyError):
        import traceback; traceback.print_exc()
        abort(404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug='--debug' in sys.argv, port=8889)
