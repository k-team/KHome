from twisted.internet import reactor
import module
import fields
import fields.io
import fields.persistant
import time



class ShutterController(module.Base)
    update_rate = 10

    shutter = use_module('Shutter')
    LuminosityInt = use_module('LuminosityInteriorSensor')
    LuminosityExt = use_module('LuminosityExteriorSensor')
    
    class Controller(
        fields.Base):
        
        def always(self):
            if LuminosityInt.Luminosity() < LuminosityInt.LuminosityLimit :
                if LuminosityInt.LuminosityLimit < LuminosityExt.Luminosity():
                    shutter.Shutter(100)
                else :
                    shutter.Shutter(0)
            elif LuminosityInt.Luminosity() == LuminosityInt.LuminosityLimit :
                    shutter.Shutter(0)    
            else :
                if LuminosityInt.LuminosityLimit < LuminosityExt.Luminosity():
                    shutter.Shutter(0)
                else :
                    shutter.Shutter(100)
        
        
    #code du main a remettre lais il était chelou donc pr le moment je l'ai vire...
