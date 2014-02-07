from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class LightButton(core.module.Base)
    update_rate = 10
    lc = use_module('LightSensor')
    la = use_module('LightActuator')

    LightButton = fields.proxy.mix('LightButton',
                                   'LightSensor','LightButton',
                                   'LightActuator','LightButton')
        
        
    #code du main a remettre lais il était chelou donc pr le moment je l'ai vire...
