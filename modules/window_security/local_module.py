import module
from module import use_module
import fields
import fields.io
import fields.proxy

class WindowSecurity(module.Base):
    update_rate = 10

    windowAccess = use_module('WindowAccess')
    recognition = use_module('Recognition')
    alarmActuator = use_module('AlarmActuator')

    security = fields.proxy.mix('Security', 'WindowAccess', 'Window',
            'Recognition', 'Recognised', 'AlarmActuator', 'Alarm')
