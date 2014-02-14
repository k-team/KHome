import module
from module import use_module
import fields


class ShutterHeatController(module.Base):
    update_rate = 10000

    shutter = use_module('Shutter')
    temperatureInt = use_module('Temperature')
    temperatureExt = use_module('TemperatureExteriorSensor')
    tempControl = use_module('TemperatureController')
    
    class controller(fields.Base):
    
  
        
        def always(self):
            try:
                tempInt = self.module.temperatureInt.temperature()[1]
                tempExt = self.module.temperatureExt.temperature()[1]
                limit= self.module.tempControl.limit()
            except TypeError:
                pass # Ignore
            else:
                if tempInt < limit:
                    if tempInt < tempExt:
                        self.module.shutter.shutter(100)
                    else :
                        self.module.shutter.shutter(0)
                else :
                    if tempInt < tempExt:
                        self.module.shutter.shutter(0)
                    else :
                        self.module.shutter.shutter(100)
