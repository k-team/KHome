import sys
import random
from twisted.python.log import startLogging
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver

class DummyTemperatureProtocol(LineReceiver):
    def lineReceived(self, line):
        print 'lineReceived', line
        if line == 'get':
            self.sendLine(str(random.random()*40%10))

if __name__ == '__main__':
    startLogging(sys.stdout)
    factory = Factory()
    factory.protocol = DummyTemperatureProtocol
    port = reactor.listenUNIX('module.sock', factory)
    reactor.run()
