# -*- coding: utf-8 -*-

import module
import fields

class MoistureSensor(module.Base):
    update_rate = 30
    public_name = 'Capteur d\' humidité'

    class sensor(fields.sensor.Moisture, fields.io.Graphable,
            fields.syntax.Numeric, fields.persistant.Database, fields.Base):
        public_name = 'Humidité (%)'
