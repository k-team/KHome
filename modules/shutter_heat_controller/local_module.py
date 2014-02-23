# -*- coding: utf-8 -*-

import module
from module import use_module
import fields.proxy
import fields

class ShutterHeatController(module.Base):
    update_rate = 10000

    shutter = use_module('Shutter')
    temperatureInt = use_module('Temperature')
    temperatureExt = use_module('Weather')
   #tempControl = use_module('TemperatureController')

    _shutter = fields.proxy.writable('Volets', 'Shutter', 'shutter')
    #_tempInt = fields.proxy.readable('Temperature Intérieur', 'Temperature', 'temperature')
    #_tempExt = fields.proxy.readable('Temperature exterieur', 'TemperatureExteriorSensor', 'temperature')
    
    class limit(
            fields.syntax.Constant,
            fields.syntax.Numeric,
            fields.Base):
        const_value = 60.0
        public_name = 'Temperature minimale à l\' intérieur'

    class controller(fields.Base):
        def always(self):
            try:
                tempInt = self.module.temperatureInt.sensor()[1]
                tempExt = self.module.temperatureExt.temperature()[1]
                print 'truc = %s' % tempExt
                limit= self.module.limit
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
