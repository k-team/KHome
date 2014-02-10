from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time
import core.all_modules.Shutter
import core.all_modules.Temperature
import core.all_modules.TemperatureForecast




if __name__ == '__main__':
class ShutterController(core.module.Base)
        shutter= use_module('Shutter')
        temp = use_module('Temperature')
        
        class Controller(
            core.fields.Base):
            
            def always(self):
                if presence.Presence() :
                    light.LightButton(true)
                else
                    light.LightButton(false)
        
        
    #code du main a remettre lais il était chelou donc pr le moment je l'ai vire...
