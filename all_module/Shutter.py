from twisted.internet import reactor
import module
import fields
import fields.io
import fields.persistant
import time

class Shutter(core.module.Base)
    update_rate = 10
    
    Shutter = fields.proxy.mix('Shutter',
                                   'Shutter','ShutterSensor',
                                   'Shutter=','ShutterActuator')
        
        
    #code du main a remettre lais il était chelou donc pr le moment je l'ai vire...
