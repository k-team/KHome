import module
from module import use_module
import fields
import fields.proxy

class ElectricCurrentController(module.Base):
    switch = use_module('ElectricCurrentSwitch')
    human_presence = use_module('HumanPresenceSensor')

    electric_current = fields.proxy.mix('ElectricCurrentController',
            'ElectricCurrent', 'HumanPresence', 'Presence')

    class controller(fields.Base):

        def __init__(self):
            super(ElectricCurrentController.controller, self).__init__()

        def always(self):
            if self.module.human_presence.presence():
               self.module.electric_current.switch(True)
            else:
               self.module.electric_current.switch(False)
