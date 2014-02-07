import module
from module import use_module
import fields.proxy

class ElectricCurrent(module.Base):
    update_rate = 10

    Room = use_module('Room')

    electric_current = fields.proxy.mix('ElectricCurrent',
            'ElectricCurrentSensor', 'ElectricCurrent',
            'ElectricCurrentActuator', 'ElectricCurrent')
