import module
from module import use_module
import fields.proxy

class ElectricCurrentController(module.Base):
    ElectricCurrent = use_module('ElectricCurrent')
    HumanPresence = use_module('HumanPresence')

    electric_current_controller = fields.proxy.mix('ElectricCurrentController',
            'ElectricCurrent', 'ElectricCurrent', 'HumanPresence', 'Presence')
