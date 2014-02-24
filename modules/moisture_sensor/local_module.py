#-*- coding: utf8 -*-
import module
import fields
import fields.io
import fields.sensor
import fields.persistant
import fields.syntax

class MoistureSensor(module.Base):
    update_rate = 10
    public_name = 'Capteur d\' humidité'

    #class sensor(fields.io.Hidden,fields.syntax.Numeric, fields.sensor.Moisture,
      #      fields.io.Graphable, fields.persistant.Database, fields.Base):
       # public_name = "Capteur d'humidite"
    class sensor(
        fields.sensor.Moisture, 
        fields.io.Graphable,
        fields.syntax.Numeric,
        fields.persistant.Database,
        fields.Base):
        public_name = 'Humidité (%)'
