from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class Recognition(core.module.Base)
    update_rate = 10
    cc = use_module('CameraSensor')
    
    Recognised = fields.proxy.mix('Recognised', 
    															'CameraSensor', 'Image')

    #code du main a remettre lais il était chelou donc pr le moment je l'ai vire...
