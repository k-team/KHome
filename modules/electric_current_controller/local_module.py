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
                print "presence = %s" % presence
            except TypeError as e:
                logger = logging.getLogger()
                logger.exception(e)
            else:
                if presence:
                   print "ouvrir courrant"
                   self.module.switch.electric_current(True)
                else:
                   print "fermer courrant"
                   self.module.switch.electric_current(False)
