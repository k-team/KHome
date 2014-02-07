import module
from module import use_module
import fields.proxy

class DoorSecurity(module.Base):
    update_rate = 10
    DoorAccess = use_module('DoorAccess')
    Recognition = use_module('Recognition')
    AlarmActuator = use_module('AlarmActuator')

    security = fields.proxy.mix('Security', 'DoorAccess', 'Door',
            'Recognition', 'Recognised', 'AlarmActuator', 'Alarm')
