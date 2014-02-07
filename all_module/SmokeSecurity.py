import module
from module import use_module
import fields.proxy

class SmokeSecurity(module.Base):
    update_rate = 10

    AlarmActuator = use_module('AlarmActuator')

    security = fields.proxy.mix('Security', 'SmokeSensor', 'Smoke',
            'AlarmActuator', 'Alarm')
