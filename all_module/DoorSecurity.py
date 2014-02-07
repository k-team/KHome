import module
from module import use_module
import fields.proxy

class DoorSecurity(module.Base):
    update_rate = 10
    door_access = use_module('DoorAccess')
    recognition = use_module('Recognition')
    alarm_actuator = use_module('AlarmActuator')

    security = fields.proxy.mix('Security', 'DoorAccess', 'Door',
            'Recognition', 'Recognised', 'AlarmActuator', 'Alarm')
