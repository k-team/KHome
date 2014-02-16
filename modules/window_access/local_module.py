import module
import fields.proxy

class WindowAccess(module.Base):
    update_rate = 10

    window = fields.proxy.mix('window', 'WindowSensor', 'window',
            'WindowActuator', 'window')
