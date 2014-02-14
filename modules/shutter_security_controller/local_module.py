import module
from module import use_module
import fields

class ShutterSecurityController(module.Base):
        update_rate = 2

        shutter= use_module('Shutter')
        presence = use_module('HumanPresenceSensor')

        
        class controller(fields.Base):
            
            def always(self):
                if not presence.presence() :
                    shutter.shutter(0)
        
