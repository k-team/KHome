# -*- coding: utf-8 -*-

import module
import fields

class MoistureSensor(module.Base):
    update_rate = 10

    class moisture(fields.syntax.Numeric, fields.sensor.Moisture,
            fields.io.Graphable, fields.persistant.Database, fields.Base):
        public_name = "Humidité"
