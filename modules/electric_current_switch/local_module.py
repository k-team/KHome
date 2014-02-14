import module
from module import use_module
import fields.proxy

class ElectricCurrentSwitch(module.Base):
    update_rate = 10
    # room = use_module('Room')
    electricCurrentSensor = use_module('ElectricCurrentSensor')
    electricCurrentActuator = use_module('ElectricCurrentActuator')

    electricCurrentSwitch = fields.proxy.mix('electric_current',
                                       'ElectricCurrentSensor', 'electric_current',
                                   	   'ElectricCurrentActuator', 'electric_current')
