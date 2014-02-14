import module
from module import use_module
import fields


class ShutterLightController(module.Base):
    update_rate = 500

    shutter = use_module('Shutter')
    LuminosityInt = use_module('LuminosityInteriorSensor')
    LuminosityExt = use_module('LuminosityExteriorSensor')
    presence = use_module('HumanPresence')
    
    class controller(fields.Base):
        
        def __init__(self):
            self.luminosity_limit = 60 # for the time being it will be a percentage
            super(Controller, self).__init__()
        
        def always(self):
            
            lumInt=LuminosityInt.Luminosity()
            lumExt=LuminosityExt.Luminosity()
            
        
            if  lumExt < 20:
                #this represent he night (so we close the shutters)
                shutter.Shutter(0)
            elif presence.presence():
                if lumInt < self.luminosityLimit :
                    if self.luminosityLimit < lumExt:
                        shutter.Shutter(100)                
