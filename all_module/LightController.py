from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time
import all_modules.LightButton
import all_modules.HumanPresence

if __name__ == '__main__':
    class LightController(core.module.Base)
        light= use_module('LightButton')
        presence= use_module('HumanPresence')
        
        class Controller(
            core.fields.Base):
            
            def always(self):
                if presence.Presence() :
                    light.LightButton(true)
                else
                    light.LightButton(false)
                
            
            
        
    #code du main a remettre mais il etait chelou donc pr le moment je l'ai vire...
