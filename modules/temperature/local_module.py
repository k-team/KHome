import module
from module import use_module
import fields.proxy

class Temperature(module.Base):
    update_rate = 10

    #room = use_module('Room')

    temperature = fields.proxy.mix('temperature',
		'TemperatureSensor', 'temperature',
		'TemperatureActuator', 'temperature')
