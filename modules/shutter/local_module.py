import module
import fields.proxy

class Shutter(module.Base):
    update_rate = 10

    # this attribute represent the value of the opening of the shutters
    # 100 is fully opened, 0 is closed
    shutter = fields.proxy.mix('shutter',
			'ShutterSensor', 'shutter',
            'ShutterActuator', 'shutter')
