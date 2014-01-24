from twisted.internet import reactor
from twisted.internet.protocol import ClientCreator
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol

class SensorConnection(Protocol):
    def __init__(self, sensor, filter_id):
        self.sensor = sensor
        self.filter_id = filter_id

    def dataReceived(self, data):
        print "Server said:", data

# Analyse
        org = data[6:8]
        value = data[8:16]
        sensor_id = data[16:24]
        status = data[24:26]

        if sensor_id == self.filter_id:
            self.sensor.emit_value(value)

class SensorConnectionFactory(ClientFactory):
    def __init__(self, sensor, filter_id):
        self.sensor = sensor
        self.filter_id = filter_id

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed - goodbye!"
# Do something ?

    def clientConnectionLost(self, connector, reason):
        print "Connection lost - goodbye!"
# Do something ?

    def buildProtocol(self, addr):
        return SensorConnection(self.sensor, self.filter_id)

class Sensor(object):
    sensor_host = '134.214.106.23'
    sensor_port = 5000
    sensor_id = 0

    def __init__(self):
        super(Sensor, self).__init__()
        reactor.connectTCP(type(self).sensor_host,
                type(self).sensor_port,
                SensorConnectionFactory(self,
                    type(self).sensor_id))

    def start(self):
        super(Sensor, self).start()

    def close(self):
        super(Sensor, self).close()

if __name__ == '__main__':
    reactor.run()
