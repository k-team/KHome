from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time
import all_modules.light_button

if __name__ == '__main__':
    class LightController(core.module.Base)
        light= use_module('LightButton')
        presence= use_module('Presence')
        
        def always(self):
            #here do action
            
            
            
        
    #code du main a remettre mais il etait chelou donc pr le moment je l'ai vire...
