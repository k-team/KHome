import sys
import json
from flask import Flask, send_file, jsonify

# configuration
with open('module.json', 'r') as fp:
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
    return send_file('rooms.json')

if __name__ == '__main__':
    app.run(debug='--debug' in sys.argv or conf.get('debug', False),
            port=int(conf.get('port', 8888)))
