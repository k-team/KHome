
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.


"""
An example client. Run simpleserv.py first before running this.
"""

import sys
from twisted.internet import reactor, protocol
from twisted.python.log import startLogging

# a client protocol

class TrameAnalyse(protocol.Protocol):
    """Once connected, send a message, then print the result."""
    def __init__(self):
        self.cpt = 0    

    def compteur(self):
        self.cpt = self.cpt+1
        print "compteur = ",self.cpt

    def connectionMade(self):
        #self.transport.write("hello, world!")
        print "Connexion etablished"
    
    def dataReceived(self, data):
        "As soon as any data is received, write it back."
        print "Server said:", data
        #self.compteur()
        self.analyser(data)
    
    def connectionLost(self, reason):
        print "connection lost"
    
    def analyser(self,data):
        print "analyse en cours: "
        #a completer
        org = data[6:8]
        valeur = data[8:16]
        id_capteur = data[16:24]
        status = data[24:26]
        print 


class EchoFactory(protocol.ClientFactory):
    protocol = TrameAnalyse

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed - goodbye!"
        reactor.stop()
    
    def clientConnectionLost(self, connector, reason):
        print "Connection lost - goodbye!"
        reactor.stop()


# this connects the protocol to a server runing on port 8000
def main():
    f = EchoFactory()
    #startLogging(sys.stdout)
    reactor.connectTCP("134.214.106.23", 5000, f)
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
