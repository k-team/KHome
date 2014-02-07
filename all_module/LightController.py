from twisted.internet import reactor
import module
import fields
import fields.io
import fields.persistant
import time


class LightController(module.Base):
    light = use_module('LightButton')
    presence = use_module('HumanPresence')
    luminosity = use_module('LuminosityInteriorSensor')
    
    class Controller(
        fields.Base):

        
        def _init_:
            luminosityLimit=60 # for the time being it will be a percentage. idk the real values
            super(Controller, self)._init_
    
        def always(self):
            if presence.Presence() :
                if luminosity.Luminosity() < luminosity.Luminosity.LuminosityLimit :
                    light.LightButton(true)
            else : 
                light.LightButton(false)
                
            
            
        
    #code du main a remettre mais il etait chelou donc pr le moment je l'ai vire...
