from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

if __name__ == '__main__':

    class ShutterCaptor(core.module.Base):
        update_rate = 10

        class Shutter(
                core.fields.sensor.Shutter
                core.fields.io.Readable,
                core.fields.persistant.Volatile,
                core.fields.Base):
            pass

    class ShutterActuator(core.module.Base):
	
        class Shutter(
            core.fields.actuator.Shutter
            core.fields.io.Writable,
            core.fields.Base):
        pass
		
	
	class Shutter(core.module.Base)
        update_rate = 10
        sc = use_module('ShutterCaptor')
        sa = use_module('ShutterActuator')

        Shutter = fields.proxy.mix('Shutter',
            'ShutterCaptor','Shutter','ShutterActuator','Shutter')
        
    class ShutterController(core.module.Base)
        shutter= use_module('Shutter')
        
        def always(self):
            shutter.
        
    #code du main a remettre lais il était chelou donc pr le moment je l'ai vire...
