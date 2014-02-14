import module
from module import use_module
import fields


class ShutterController(module.Base):
    update_rate = 10000

    shutter = use_module('Shutter')
    temperatureInt = use_module('Temperature')
    temperatureExt = use_module('TemperatureExteriorSensor')
    tempControl = use_module('TemperatureController')
    
    class controller(fields.Base):
    
        tempInt = temperatureInt.temperature()
        tempExt = temperatureEnt.temperature()
        
        def always(self):
            if tempInt < tempControl.seuil :
                if tempInt < tempExt:
                    shutter.shutter(100)
                else :
                    shutter.shutter(0)
            else :
                if tempInt < tempExt:
                    shutter.shutter(0)
                else :
                    shutter.shutter(100)