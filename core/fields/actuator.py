import io
import syntax
import persistant

def Dummy(data_type):
    class _Dummy(data_type,
            io.Readable,
            persistant.Volatile,
            io.Writable):
        def set_value(self, value):
            print value
    return _Dummy


Alarm = Dummy(syntax.Boolean)
Door = Dummy(syntax.Boolean)
ElectricCurrent = Dummy(syntax.Boolean)
Fan = Dummy(syntax.Boolean)
Gaz = Dummy(syntax.Boolean) #true = ouvert, flase = ferme
LightButton = Dummy(syntax.Boolean)
Piston = Dummy(syntax.Boolean)
Shutter = Dummy(syntax.Numeric)
Temperature = Dummy(syntax.Numeric)
WaterValve = Dummy(syntax.Boolean)
Window = Dummy(syntax.Boolean)


import sys
import string
from twisted.internet import protocol
from twisted.python.log import startLogging
from twisted.internet import reactor
from twisted.internet.protocol import ClientCreator
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
import time
import math
import random
import time

class Actuator(object):
    from twisted.internet import reactor
    #host = '134.214.106.23'
    #port = 5000
    host = '134.214.106.23'
    port = 5000
    actuator_id = ""
    org =""
    sentData=""
    connector=""

    def __init__(self):
        super(Actuator, self).__init__()
        reactor.connectTCP(type(self).host,
                type(self).port,
                ActuatorConnectionFactory(self,
                    type(self).actuator_id))


    def sendData(self,data):
        pass

    def start(self):
        self.connector = reactor.run()
        #super(Actuator, self).start()

    def close(self):
        self.connector.disconnect()
        #protocol.transport.loseConnection()
        #reactor.stop()
        super(Actuator, self).close()
        
        
        
        
class ActuatorConnection(Protocol):
    def __init__(self, actuator):
        self.actuator = actuator
        
    def connectionMade(self):
        print "Connexion etablished"
        self.transport.write(self.actuator.sentData)
        # self.transport.loseConnection()
        # reactor.stop()
        #self.transport.write(self.actuator.sentData)

    def dataReceived(self, data):
        "As soon as any data is received, write it back."
        print "Server said:", data
    def sendData(self):
        self.transport.write(self.actuator.sentData)

    def connectionLost(self, reason):
        print "connection lost"
        
        
class ActuatorConnectionFactory(ClientFactory):
    def __init__(self, actuator,filter_id):
        self.actuator = actuator
        self.filter_id = filter_id

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed - goodbye!"

    def clientConnectionLost(self, connector, reason):
        print "Connection lost - goodbye!"

    def buildProtocol(self, addr):
        return ActuatorConnection(self.actuator)
        
        
        
class PriseElectrique(Actuator):
    actuator_id = "00893378"
    org = "05"
    
    
    def sendData(self,data):
        stat_check = "308E"
        if data=="1": #activer
            data = "50000000"
        else:
            data = "70000000"
        self.sentData = "A55A6B"+self.org+data+self.actuator_id+stat_check  
        self.start()
        #self.stop()

if __name__ == '__main__':
   a = PriseElectrique()
   a.sendData("1")

