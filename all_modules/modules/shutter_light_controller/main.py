from twisted.internet import reactor
import module
import fields
import fields.io
import fields.persistant
import time



class ShutterController(module.Base)
    update_rate = 10


    
    class Controller(fields.Base):
        
        shutter = use_module('Shutter')
        luminosityInt = use_module('LuminosityInteriorSensor')
        luminosityExt = use_module('LuminosityExteriorSensor')
        humPres = use_module('HumanPresenceSensor')
        cur_lum_ext = luminosityExt.luminosity()
        cur_lum_int = luminosityInt.luminosity()
        
        def always(self):
            if cur_lum_int < luminosityExt.NIGHTLIMIT : 
                shutter.Shutter(0)
            else:
                if cur_lum_int < luminosityInt.luminosityLimit :
                    if luminosityInt.luminosityLimit < cur_lum_ext:
                        shutter.Shutter(100)
                    else :
                        shutter.Shutter(0)
                elif cur_lum_int == luminosityInt.luminosityLimit :
                        shutter.Shutter(0)    
                else :
                        shutter.Shutter(0)
        
        
