import module
from module import use_module
import fields
import fields.io
import fields.proxy

class WindowAccess(module.Base):
    update_rate = 10

    WindowSensor = use_module('WindowSensor')
    WindowActuator = use_module('WindowActuator')

    window = fields.proxy.mix('Window', 'WindowSensor', 'Window',
            'WindowActuator', 'Window')
