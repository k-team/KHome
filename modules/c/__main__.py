import os
from twisted.web import server, resource
from twisted.internet import reactor

moduleName = os.path.basename(os.path.dirname(os.path.realpath(__file__)))

class ModuleResource(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        request.setHeader('content-type', 'text/plain')
        return 'Module "%s"\n' % moduleName

if __name__ == '__main__':
    with open('address.txt', 'r') as fp:
        address = int(fp.read().strip('\r\n'))
    reactor.listenTCP(address, server.Site(ModuleResource()))
    reactor.run()
