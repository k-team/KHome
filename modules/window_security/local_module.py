import module
from module import use_module
import fields
import fields.io
import fields.proxy

class WindowSecurity(module.Base):
    update_rate = 10

    WindowAccess = use_module('WindowAccess')
    Recognition = use_module('Recognition')
    AlarmActuator = use_module('AlarmActuator')

    security = fields.proxy.mix('Security', 'WindowAccess', 'Window',
            'Recognition', 'Recognised', 'AlarmActuator', 'Alarm')
