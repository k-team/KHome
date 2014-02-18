import module
from module import use_module
import fields.proxy

class ElectricCurrentSwitch(module.Base):
    update_rate = 10
    electric_current = fields.proxy.mix('electric_current',
                                       'ElectricCurrentSensor', 'electric_current',
                                   	   'ElectricCurrentActuator', 'electric_current')
