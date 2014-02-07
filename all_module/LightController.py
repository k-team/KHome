from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

if __name__ == '__main__':
    class LightController(core.module.Base)
        light = use_module('LightButton')
        presence = use_module('HumanPresence')
        luminosity = use_module('LuminosityInteriorSensor')
        
        class Controller(
            core.fields.Base):
            
            def _init_:
                luminosityLimit=60 # for the time being it will be a percentage. idk the real values
                super(Luminosity, self)._init_
        
            def always(self):
                if presence.Presence() :
                    if luminosity.Luminosity() < luminosity.Luminosity.LuminosityLimit :
                        light.LightButton(true)
                else
                    light.LightButton(false)
                
            
            
        
    #code du main a remettre mais il etait chelou donc pr le moment je l'ai vire...
