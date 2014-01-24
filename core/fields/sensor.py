from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint as ServerEndpoint

class SensorConnection(Protocol):
    def __init__(self, sensor, id_filter):
        self.sensor = sensor
        self.id_filter = id_filter

    def dataReceived(self, data):
        print "Server said:", data

# Analyse
        org = data[6:8]
        value = data[8:16]
        id_sensor = data[16:24]
        status = data[24:26]

        if id_sensor == self.id_filter:
            self.sensor.emit_value(value)

class SensorConnectionFactory(ClientFactory):
    def __init__(self, sensor):
        self.sensor = sensor

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed - goodbye!"
# Do something ?

    def clientConnectionLost(self, connector, reason):
        print "Connection lost - goodbye!"
# Do something ?

    def buildProtocol(self, addr):
        return SensorConnection(self.sensor)

class Sensor(object):
    sensor_address = '134.214.106.23'
    sensor_port = 5000

    def __init__(self):
        self.reactor = reactor # do something
        self.endpoint = ServerEndpoint(self.reactor,
                type(self).sensor_address, type(self).sensor_port)
        self.endpoint.listen(SensorConnectionFactory(self))

    def start(self):
        self.reactor.run()
        super(Sensor, self).start()

    def close(self):
        self.reactor.close()
        super(Sensor, self).close()
