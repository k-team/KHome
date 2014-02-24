# -*- coding: utf-8 -*-

import module
import fields

class LuminosityExteriorSensor(module.Base):
    update_rate = 10
    public_name = 'Luminosité extérieure'

    class luminosity_exterior(fields.syntax.Numeric,
            fields.sensor.LuminosityExterior, fields.io.Graphable,
            fields.persistant.Volatile, fields.Base):
        public_name = 'Luminosite extérieure (lux)'
