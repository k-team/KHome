import module
from module import use_module
import fields
import fields.proxy
import logging

class ElectricCurrentController(module.Base):
    switch = use_module('ElectricCurrentSwitch')
    human_presence = use_module('HumanPresenceSensor')

    class controller(fields.Base):
        def __init__(self):
            super(ElectricCurrentController.controller, self).__init__()

        def always(self):
            try:
                presence = self.module.human_presence.presence()[1]
            except TypeError as e:
                logger = logging.getLogger()
                logger.exception(e)
            else:
                if presence:
                   self.module.electric_current.switch(True)
                else:
                   self.module.electric_current.switch(False)
