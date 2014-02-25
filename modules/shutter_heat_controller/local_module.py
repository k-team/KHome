# -*- coding: utf-8 -*-

import module
from module import use_module
import fields

class ShutterHeatController(module.Base):
    update_rate = 60 * 10

    public_name = 'Aération'

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
            fields.syntax.Numeric,
            fields.persistant.Database,
            fields.Base):
        public_name = 'Température min à l\'intérieur'

        def on_start(self):
            super(ShutterHeatController.limit, self).on_start()
            if self.module.limit() is None:
                self.emit_value(60.0)

    class controller(fields.Base):
        def always(self):
            try:
                tempInt = self.module.temperatureInt.sensor()[1]
                tempExt = self.module.temperatureExt.temperature()[1]
                limit = self.module.limit
            except TypeError:
                pass # Ignore
            else:
                if tempInt < limit:
                    if tempInt < tempExt:
                        self.module.shutter.shutter(100)
                    else:
                        self.module.shutter.shutter(0)
                else:
                    if tempInt < tempExt:
                        self.module.shutter.shutter(0)
                    else:
                        self.module.shutter.shutter(100)
