import module
import fields
from module import use_module

class WaterFlushController(module.Base):
    update_reate = 10
    """ todo  """
    water_flush = use_module('WaterFlush')
    human_presence = use_module('HumanPresenceSensor')
    class controller(fields.Base):

        def __init__(self):
            super(WaterFlushController.controller, self).__init__()
        
        def always(self):
            if self.module.water_flush.flush():
                self.module.water_flush.flush('')
            else:
                self.module.water_flush.flush('NOT')
