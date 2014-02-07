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
                                   'Shutter','ShutterActuator'):
        '''this attribute represent the value of the opening of the shutters
            100 is fully opened, 0 is closed'''
            pass
        
        
    #code du main a remettre lais il était chelou donc pr le moment je l'ai vire...
