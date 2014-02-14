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
            self.luminosity_limit = 60 # this represent the luminosity the user want in the room
            self.night_limit = 20 # this represent the luminosity limit to know if it is the night
            super(controller, self).__init__()
        
        def always(self):
            
            lumInt=LuminosityInt.luminosity()
            lumExt=LuminosityExt.luminosity()
            
        
            if  lumExt < self.night_limit:
                #this represent he night (so we close the shutters)
                shutter.shutter(0)
            elif presence.presence():
                if lumInt < self.luminosityLimit :
                    if self.luminosityLimit < lumExt:
                        shutter.shutter(100)                
