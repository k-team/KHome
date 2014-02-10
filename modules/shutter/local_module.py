import module
from module import use_module
import fields.proxy

class Shutter(module.Base)
    update_rate = 10

    shutter_sensor = use_module('ShutterSensor')
    shutter_actuator = use_module('ShutterActuator')

    # this attribute represent the value of the opening of the shutters
    # 100 is fully opened, 0 is closed
    shutter = fields.proxy.mix('shutter', 'Shutter', 'ShutterSensor',
            'Shutter', 'ShutterActuator'):
