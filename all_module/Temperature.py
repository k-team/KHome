from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class Temperature(core.module.Base):
    update_rate = 10
    room = use_module('Room')
    Temperature = fields.proxy.mix('Temperature',
                                   'TemperatureSensor', 'Temperature',
                                   'TemperatureActuator', 'Temperature')
