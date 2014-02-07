from twisted.internet import reactor
import module
import fields
import fields.io
import fields.persistant
import time



class ShutterController(module.Base)
    update_rate = 10

    shutter = use_module('Shutter')
    tempInt = use_module('Temperature')
    tempExt = use_module('TemperatureExteriorSensor')
    
    class Controller(
        fields.Base):
        
        def always(self):
            if tempInt.Temperature() < tempInt.seuil :
                if tempInt.Temperature() < tempExt.Temperature():
                    shutter.Shutter(100)
                else :
                    shutter.Shutter(0)
            elif tempInt.Temperature() == tempInt.seuil :
                    shutter.Shutter(0)    
            else :
                if tempInt.Temperature() < tempExt.Temperature():
                    shutter.Shutter(0)
                else :
                    shutter.Shutter(100)
    
#code du main a remettre lais il était chelou donc pr le moment je l'ai vire...
