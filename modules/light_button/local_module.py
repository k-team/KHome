import module
import fields.proxy

class LightButton(module.Base):
    update_rate = 10

    light_button = fields.proxy.mix('light_button',
            'LightButtonSensor','light_button',
            'LightButtonActuator','light_button')
