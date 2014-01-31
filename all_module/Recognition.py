from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

if __name__ == '__main__':
    
	class Recognition(core.module.Base)
        update_rate = 10
        cc = use_module('CapteurCamera')
        
        Recognised = fields.proxy.mix('Recognised',
            'CapteurCamera','Image')

    b = M1()

    b.start()
    reactor.run()
    b.stop()
    b.join(1)
