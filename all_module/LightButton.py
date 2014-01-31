from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

if __name__ == '__main__':
    class LightCaptor(core.module.Base):
        update_rate = 10

        class LightButton(
                core.fields.sensor.LightInterruptor
                core.fields.io.Readable,
                core.fields.persistant.Volatile,
                core.fields.Base):
            pass

    class LightActuator(core.module.Base):
	
        class LightButton(
            core.fields.actuator.LightInterruptor
            core.fields.io.Writable,
            core.fields.Base):
        pass
		
	
	class LightButton(core.module.Base)
        update_rate = 10
        lc = use_module('LightCaptor')
        la = use_module('LightActuator')

        LightButton = fields.proxy.mix('LightButton',
            'LightCaptor','LightButton','LightActuator','LightButton')
        
        
    #code du main a remettre lais il était chelou donc pr le moment je l'ai vire...
