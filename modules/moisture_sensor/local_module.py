import module
import fields
import fields.io
import fields.sensor
import fields.persistant
import fields.syntax
import logging

class MoistureSensor(module.Base):
    update_rate = 10

    class _moisture(fields.io.Hidden,fields.syntax.Numeric, fields.sensor.Moisture,
            fields.io.Graphable, fields.persistant.Database, fields.Base):
        public_name = "Capteur d'humidite"
