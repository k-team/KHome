import module
from module import use_module
import fields.proxy

class LightButton(module.Base)
    update_rate = 10

    LightSensor = use_module('LightSensor')
    LightActuator = use_module('LightActuator')

    light_button = fields.proxy.mix('LightButton', 'LightSensor','LightButton',
            'LightActuator','LightButton')
