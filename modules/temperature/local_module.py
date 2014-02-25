# -*- coding: utf-8 -*-

import module
import fields

class Temperature(module.Base):
    update_rate = 3
    public_name = 'Temperature'

    class sensor(fields.sensor.Temperature, fields.io.Graphable,
            fields.syntax.Numeric, fields.persistant.Database, fields.Base):
        public_name = 'Thermomètre (°C)'

    class actuator(
            fields.actuator.Temperature,
            fields.io.Readable,
            fields.io.Writable,
            fields.syntax.Numeric,
            fields.persistant.Volatile,
            fields.Base):
        public_name = 'Radiateur (°C)'
