import module
import fields.proxy

class LightButton(module.Base):
    update_rate = 10

    light_button = fields.proxy.mix('LightButton',
            'LightButtonSensor','LightButton',
            'LightButtonActuator','LightButton')
