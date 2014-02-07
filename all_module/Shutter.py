import module
from module import use_module
import fields.proxy

class Shutter(module.Base)
    update_rate = 10

    shutter_sensor = use_module('ShutterSensor')
    shutter_actuator = use_module('ShutterActuator')

    shutter = fields.proxy.mix('Shutter', 'ShutterSensor', 'ShutterActuator')
