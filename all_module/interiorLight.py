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
		
	
	class Light(core.module.Base)
        update_rate = 10
        lc = use_module('LightCaptor')
        la = use_module('LightActuator')

        LightButton = fields.proxy.mix('LightButton',
            'LightCaptor','LightButton','LightActuator','LightButton')
        
        
    #je ne sais pas quoi definir car cette clase n'a pas d'attributs...
    #juste une action théoriquement
    class AutomaticLight(core.module.Base)
        update_rate = 10
        lc = use_module('LightButton')
        pp = use_module('PresencePersonne')
        
        
         def _act(self):
            if (lc.LightInterruptor() and pp.personne()):
                la.LightInterruptor()
                

    b = M1()

    b.start()
    reactor.run()
    b.stop()
    b.join(1)
