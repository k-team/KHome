import module
from module import use_module
import fields
import fields.io
import fields.proxy

class WindowAccess(module.Base):
    update_rate = 10

    window = fields.proxy.mix('window', 'WindowSensor', 'window',
            'WindowActuator', 'window')
