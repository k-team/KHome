# -*- coding: utf-8 -*-

import module
import fields

class LuminosityInteriorSensor(module.Base):
    update_rate = 10
    public_name = 'Capteur luminosité intérieure'

    class luminosity_interior(fields.syntax.Numeric,
            fields.sensor.LuminosityInterior, fields.io.Graphable,
            fields.persistant.Volatile, fields.Base):
        public_name = 'Luminosité intérieure (lux)'
