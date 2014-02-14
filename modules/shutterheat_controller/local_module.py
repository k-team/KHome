import module
from module import use_module
import fields

class ShutterController(module.Base):
    update_rate = 10

    shutter = use_module('Shutter')
    tempInt = use_module('Temperature')
    tempExt = use_module('TemperatureExteriorSensor')
    
    class controller(fields.Base):
        
        def __init__(self):
            super(ShutterController.controller, self).__init__()

        def always(self):
            if self.module.tempInt.temperature() < self.module.tempInt.seuil :
                if self.module.tempInt.temperature() < self.module.tempExt.temperature():
                    self.module.shutter.shutter(100)
                else :
                    self.module.shutter.shutter(0)
            elif self.module.tempInt.temperature() == self.module.tempInt.seuil :
                    self.module.shutter.shutter(0)    
            else :
                if self.module.tempInt.temperature() < self.module.tempExt.temperature():
                    self.module.shutter.shutter(0)
                else :
                    self.module.shutter.shutter(100)
    
#code du main a remettre lais il était chelou donc pr le moment je l'ai vire...
