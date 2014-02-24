# -*- coding: utf-8 -*-

import module
import fields
import fields.io
import fields.actuator
import fields.sensor
import fields.syntax
import fields.persistant

class Temperature(module.Base):
    update_rate = 3
    public_name = 'Temperature'

    class sensor(
            fields.sensor.Temperature, 
            fields.io.Graphable,
            fields.syntax.Numeric,
            fields.persistant.Database,
            fields.Base):
        public_name = 'Thermometre (°C)'

    class actuator(
            fields.actuator.Temperature,
            fields.io.Readable,
            fields.syntax.Numeric,
            fields.persistant.Volatile,
            fields.Base):
        public_name = 'Radiateur (°C)'
