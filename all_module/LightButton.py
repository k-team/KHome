from twisted.internet import reactor
import module
import fields
import fields.io
import fields.persistant
import time
import all_modules.LightButtonSensor
import all_modules.LightButtonActuator

class LightButton(core.module.Base)
    update_rate = 10
    
    LightButton = fields.proxy.mix('LightButton',
                                   'LightButtonSensor','LightButton',
                                   'LightButtonActuator','LightButton')
        
        
    #code du main a remettre lais il était chelou donc pr le moment je l'ai vire...
