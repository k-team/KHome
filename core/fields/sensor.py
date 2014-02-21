import sys
import time
import math
import random
import logging

_cd = sys.path.pop(0)
from twisted.internet import reactor
from twisted.internet.protocol import ClientCreator, ClientFactory, Protocol
sys.path.insert(0, _cd)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
_formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
_handler = logging.StreamHandler()
_handler.setFormatter(_formatter)
_handler.setLevel(logging.DEBUG)
logger.addHandler(_handler)

def Dummy(dummy_funct):
    """
    Return a class generating dummy data describe by the *dummy_funct*
    function. *dummy_funct* receive the time as parameter and return one value
    """

    class _Dummy(object):
        def acquire_value(self):
            return dummy_funct(time.time())
    return _Dummy

#TemperatureSensor = Dummy(lambda t:
#        math.sin(t) * 15 + 20 + 0.5 * (random.random() - 0.5))

#DoorSensor = Dummy(True if random.random() > 0.5 else False)


Air = Dummy(lambda t:
        math.sin(t) * 30 + 30 + 0.5 * (random.random() - 0.5))

Butane = Dummy(lambda t:
        math.sin(t) * 1500 + 2000 + 0.5 * (random.random() - 0.5)) #seuil 1500

CO = Dummy(lambda t:
        math.sin(t) * 200 + 200 + 0.5 * (random.random() - 0.5)) # seuil 60

Camera = Dummy(lambda t:
        math.sin(t) * 15 + 20 + 0.5 * (random.random() - 0.5))

ElectricCurrent = Dummy(lambda t: True if random.random() > 0.5 else False)

LightButton = Dummy(lambda t: True if random.random() > 0.5 else False)

Presence = Dummy(lambda t: True if random.random() > 0.5 else False)

LuminosityExterior = Dummy(lambda t:
        (math.sin(t)+1) * 50 ) # this will vary between 0 and 100

LuminosityInterior = Dummy(lambda t:
        (math.sin(t)+1) * 50 ) # this will vary between 0 and 100

Methane = Dummy(lambda t:
        math.sin(t) * 600 + 800 + 0.5 * (random.random() - 0.5)) # seuil max 1000

Moisture = Dummy(lambda t:
        math.sin(t) * 20 + 35 + 0.5 * (random.random() - 0.5)) # seuil max 45

Propane = Dummy(lambda t:
        math.sin(t) * 1500 + 2000 + 0.5 * (random.random() - 0.5)) # seuil 1500

RainForecast = Dummy(lambda t: True if random.random() > 0.5 else False)

Shutter = Dummy(lambda t:
        math.sin(t) * 50 + 50 + 0.5 * (random.random() - 0.5))

Smoke = Dummy(lambda t:
        math.sin(t) * 15 + 20 + 0.5 * (random.random() - 0.5))

Sound = Dummy(lambda t:
        math.sin(t) * 60 + 60 + 0.5 * (random.random() - 0.5)) #seuil cri nourison fixe a 97dBl

#this one is for the interior temperature
Temperature = Dummy(lambda t:
        math.sin(t) * 15 + 20 + 0.5 * (random.random() - 0.5))

TemperatureForecast = Dummy(lambda t:
        math.sin(t) * 15 + 20 + 0.5 * (random.random() - 0.5))

TemperatureExterior = Dummy(lambda t:
        math.sin(t) * 15 + 20 + 0.5 * (random.random() - 0.5))

Window = Dummy(lambda t:
        math.sin(t) * 15 + 20 + 0.5 * (random.random() - 0.5))

WaterValve = Dummy(lambda t:
        math.sin(t) * 15 + 20 + 0.5 * (random.random() - 0.5))

class SensorConnection(Protocol):
    def __init__(self, sensor, filter_id):
        self.sensor = sensor
        self.filter_id = filter_id

    def connectionMade(self):
        logger.info('sensor connection established')

    def dataReceived(self, data):
        logger.info('raw data received %s', data)
        try:
            org = data[6:8]
            value = '{0:032b}'.format(int(data[8:16], 16))
            sensor_id = data[16:24]
            status = '{0:08b}'.format(int(data[24:26], 16))
            checksum = '{0:08b}'.format(int(data[26:28], 16))
            #A55A0B 07 A621000D 00053F44 00 6E
            #A55A0B 07 A624000F 00053F44 0073
        except (ValueError, IndexError) as e:
            logger.exception(e)

        # don't handle data where not with our sensor's id
        if sensor_id != self.filter_id:
            return
        logger.info('server sent update')

        # format data
        formatted_data = None
        if org == '05':
            formatted_data = self.org5(value, status)
        elif org == '06':
            formatted_data = self.org6(value)
        elif org == '07':
            if sensor_id[4:8] == '3E7B': # brightness
                formatted_data = self.org7_bp(value)
            elif sensor_id == '00893378': # temperature and moisture
                formatted_data = self.org7_tm(value)

        # return formatted data
        if formatted_data is not None:
            logger.info('emitting data %s', formatted_data)
            self.sensor.emit_value(formatted_data)
        else:
            logger.warning('no formatted data followed the server input')

    def org7_bp(self, value):
        """
        Brightness/Presence formatting.
        """
        brightness = int(value[16:24], 2)*510/255
        presence = value[6] == '0'
        return brightness, presence

    def org7_tm(self, value):
        """
        Temperature/Moisture formatting.
        """
        moisture = int(value[16:24], 2)*100/250
        if value[6] == '0':
            temp = -1
        else:
            temp = int(value[8:16], 2)*40/250
        return temp, moisture

    def org6(self, value):
        """
        Window "close" detection formatting.
        """
        return value[31] != '0'

    def org5(self, value, status):
        """
        Interruptor formatting.
        """
        if status[3] != '1':
            return 0b0000
        b1 = value[0:3]
        if value[7] == '0' and value[3] == '1':
            return self.findButton(b1)
        elif value[7] == '1':
            b2 = value[4:7]
            return self.findButton(b1) | self.findButton(b2)

    def findButton(self, bits):
        if   bits == '001': return 0b1000
        elif bits == '000': return 0b0100
        elif bits == '010': return 0b0001
        elif bits == '011': return 0b0010
        else:               return 0b0000

class SensorConnectionFactory(ClientFactory):
    def __init__(self, sensor, filter_id):
        self.sensor = sensor
        self.filter_id = filter_id

    def buildProtocol(self, addr):
        return SensorConnection(self.sensor, self.filter_id)

class Sensor(object):
    sensor_host = '134.214.106.23'
    sensor_port = 5000
    sensor_id = ''

    def __init__(self):
        super(Sensor, self).__init__()
        reactor.connectTCP(type(self).sensor_host, type(self).sensor_port,
                SensorConnectionFactory(self, type(self).sensor_id))

class Interruptor(Sensor):
    sensor_id = '0021CC31'

class Contact(Sensor):
    sensor_id = '0001B595'

class Brightness(Sensor):
    sensor_id = '00063E7B'

    def org7_bp(self, value):
        return super(Brightness, self).org7_bp()[0]

class Presence(Sensor):
    sensor_id = '00063E7B'

    def org7_bp(self, value):
        return super(Presence, self).org7_bp()[1]

class Moisture(Sensor):
    sensor_id = '00893378'

    def org7_tm(self, value):
        return super(Moisture, self).org7_tm()[1]

class Temperature(Sensor):
    sensor_id = '00893378'

    def org7_tm(self, value):
        return super(Temperature, self).org7_tm()[0]
