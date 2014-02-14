import time
import math
import random
from twisted.internet import reactor
from twisted.internet.protocol import ClientCreator
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol

def Dummy(dummy_funct):
    """
    Return a class generating dummy data describe by the *dummy_funct* function.
    *dummy_funct* receive the time as parameter and return one value
    """

    class _Dummy(object):
        def acquire_value(self):
            return dummy_funct(time.time())
    return _Dummy

# TemperatureSensor = Dummy(lambda t:
#         math.sin(t) * 15 + 20 + 0.5 * (random.random() - 0.5))

#DoorSensor = Dummy(
#        True if random.random() > 0.5 else False)


Air = Dummy(lambda t:
        math.sin(t) * 30 + 30 + 0.5 * (random.random() - 0.5))

Butane = Dummy(lambda t:
        math.sin(t) * 1500 + 2000 + 0.5 * (random.random() - 0.5)) #seuil 1500

CO = Dummy(lambda t:
        math.sin(t) * 200 + 200 + 0.5 * (random.random() - 0.5)) # seuil 60

Camera = Dummy(lambda t:
        math.sin(t) * 15 + 20 + 0.5 * (random.random() - 0.5))

ElectricCurrent = Dummy(lambda t:
        True if random.random() > 0.5 else False)

LightButton = Dummy(lambda t:
        True if random.random() > 0.5 else False)

LuminosityExterior = Dummy(lambda t:
        math.sin(t) * 800 + 820 + 0.5 * (random.random() - 0.5)) #seuil a fixer

Methane = Dummy(lambda t:
        math.sin(t) * 600 + 800 + 0.5 * (random.random() - 0.5)) #seuil max 1000

Moisture = Dummy(lambda t:
        math.sin(t) * 20 + 35 + 0.5 * (random.random() - 0.5)) #seuil max 45

OutsideBrightness = Dummy(lambda t:
        math.sin(t) * 800 + 820 + 0.5 * (random.random() - 0.5)) #seuil a fixer

Propane = Dummy(lambda t:
        math.sin(t) * 1500 + 2000 + 0.5 * (random.random() - 0.5)) #seuil 1500

RainForecast = Dummy(lambda t:
        True if random.random() > 0.5 else False)

Shutter = Dummy(lambda t:
        math.sin(t) * 50 + 50 + 0.5 * (random.random() - 0.5))

Smoke = Dummy(lambda t:
        math.sin(t) * 15 + 20 + 0.5 * (random.random() - 0.5))

Sound = Dummy(lambda t:
        math.sin(t) * 60 + 60 + 0.5 * (random.random() - 0.5)) #seuil cri nourison fixe a 97dBl

TemperatureForecast = Dummy(lambda t:
        math.sin(t) * 15 + 20 + 0.5 * (random.random() - 0.5))

TemperatureExterior = Dummy(lambda t:
        math.sin(t) * 15 + 20 + 0.5 * (random.random() - 0.5))




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
