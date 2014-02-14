import module
import fields
from module import use_module
import logging

class WaterFlushController(module.Base):
    update_reate = 10
    water_flush = use_module('WaterFlush')
    human_presence = use_module('HumanPresenceSensor')
    class controller(fields.Base):

        def __init__(self):
            super(WaterFlushController.controller, self).__init__()
        
        def always(self):
            try:
                flush = self.module.water_flush.flush()[1]
            except TypeError as e:
                logger = logging.getLogger()
                logger.exception(e)
            else:
                if flush:
                    self.module.water_flush.flush('')
                else:
                    self.module.water_flush.flush('NOT')
