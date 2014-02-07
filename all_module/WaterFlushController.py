import module
import fields
import fields.io
import fields.persistant
import fields.proxy
import fields.sensor
import fields.actuator
from module import use_module

class WaterFlushController(core.module.Base)
    update_reate = 10
    """ todo  """
    water_flush = use_module('WaterFlush')
    human_presence = use_module('HumanPresenceSensor')
    class controller(core.fields.Base):
        def always(self):
            if water_flush.Flush():
                water_flush.Flush('')
            else:
                water_flush.Flush('NOT')
