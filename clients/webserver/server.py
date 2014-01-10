import json
from twisted.web.server import Site
from twisted.web.static import File
from twisted.internet import reactor

# configuration
with open('client.json', 'r') as fp:
    conf = json.load(fp)
static_dir = conf.get('static_directory', 'static')
port = int(conf.get('port', 8888))

# static file server
resource = File(static_dir)
factory = Site(resource)
reactor.listenTCP(port, factory)
reactor.run()
