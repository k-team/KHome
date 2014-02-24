# -*- coding: utf-8 -*-

import module
# -*- coding: utf-8 -*-
import module
import fields
import fields.syntax
import fields.io
import fields.proxy
from module import use_module
import logging

class ShutterHeatController(module.Base):
    update_rate = 10000

    public_name = 'Controlleur d aération'

    shutter = use_module('Shutter')
    temperatureInt = use_module('Temperature')
    temperatureExt = use_module('Weather')
   #tempControl = use_module('TemperatureController')

    volet = fields.proxy.basic('shutter', 'Shutter', 'shutter')
    interior = fields.proxy.basic('sensor', 'Temperature', 'sensor')
    exterior = fields.proxy.basic('temperature', 'Weather', 'temperature')
    
    class limit(
            fields.io.Readable, 
            fields.io.Writable,
            #fields.syntax.Constant,
            fields.syntax.Numeric,
            fields.Base):
        const_value = 60.0
        public_name = 'Temperature minimale à l intérieur'

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
