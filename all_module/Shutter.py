import module
from module import use_module
import fields.proxy

class Shutter(module.Base)
    update_rate = 10

    ShutterSensor = use_module('ShutterSensor')
    ShutterActuator = use_module('ShutterActuator')

    shutter = fields.proxy.mix('Shutter', 'ShutterSensor', 'ShutterActuator')
