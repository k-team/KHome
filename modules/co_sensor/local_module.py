#-*- coding: utf-8 -*-

import module
from module import use_module
import fields

class COSensor(module.Base):
    update_rate = 1000
    public_name = 'Capteur CO'

    alarm = use_module('Alarm')

    class co(fields.sensor.CO,
            fields.syntax.Numeric,
            fields.io.Graphable,
            fields.persistant.Database,
            fields.Base):
        update_rate = 60
        public_name = 'Taux de CO (ppm)'

    class limit_value_co(
            fields.syntax.Numeric,
            fields.io.Readable,
            fields.persistant.Database,
            fields.Base):
        public_name = 'Limite CO (ppm)'
        init_value = 5.00

    class message_co(
            fields.syntax.String,
            fields.io.Readable,
            fields.io.Writable,
            fields.persistant.Database,
            fields.Base):
        public_name = 'Message d\'alerte CO'
        init_value = 'Au #secours il y a la masse de #CO #YOLO #pompier'

    class security(fields.Base):
        update_rate = 60

        def always(self):
            try:
                sensor = self.module.co()[1]
                lie = self.module.limit_value_co()[1]
                message = self.module.message_co()[1]
            except TypeError:
                pass
            else:
                if sensor > lie:
                    self.module.alarm.message(message)
