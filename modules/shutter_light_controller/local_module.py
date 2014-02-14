import module
from module import use_module
import fields

class ShutterController(module.Base)
    update_rate = 10
    
    class controller(fields.Base):
        
        shutter = use_module('Shutter')
        luminosityInt = use_module('LuminosityInteriorSensor')
        luminosityExt = use_module('LuminosityExteriorSensor')
        humPres = use_module('HumanPresenceSensor')
        def __init__(self):
            self.cur_lum_ext = self.module.luminosityExt.luminosity()
            self.cur_lum_int = self.module.luminosityInt.luminosity()
            super(ShutterController.controller, self).__init__()

        def always(self):
            if self.module.cur_lum_int < self.module.luminosityExt.night_limit : 
                self.module.shutter.shutter(0)
            else:
                if self.module.cur_lum_int < self.module.luminosityInt.luminosity_limit :
                    if self.module.luminosityInt.luminosity_limit < self.module.cur_lum_ext:
                        self.module.shutter.shutter(100)
                    else:
                        self.module.shutter.shutter(0)
                elif self.module.cur_lum_int == self.module.luminosityInt.luminosity_limit :
                        self.module.shutter.shutter(0)    
                else:
                        self.module.shutter.shutter(0)
        
        
