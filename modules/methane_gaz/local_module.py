#-*- coding: utf-8 -*-

import module
from module import use_module
import fields

class MethaneGaz(module.Base):
    update_rate = 1000
    public_name = 'Méthane'

    alarm = use_module('Alarm')

    class methane(fields.sensor.Methane,
            fields.syntax.Numeric,
            fields.io.Graphable,
            fields.persistant.Database,
            fields.Base):
        update_rate = 60
        public_name = 'Taux de méthane (% dans l\'air)'

    class limit_value_meth(
            fields.syntax.Numeric,
            fields.io.Readable,
            fields.persistant.Database,
            fields.Base):
        public_name = 'LIE Méthane'
        init_value = 5.00

    class message_meth(
            fields.syntax.String,
            fields.io.Readable,
            fields.io.Writable,
            fields.persistant.Database,
            fields.Base):
        public_name = 'Message d\'alerte methane'
        init_value = 'Au #secours il y a la masse de #methane #YOLO'

    class meth_actuator(fields.actuator.Methane, fields.syntax.Boolean,
            fields.io.Readable, fields.persistant.Volatile, fields.Base):
        public_name = 'Vanne de méthane'

    class security(fields.Base):
        update_rate = 60

        def always(self):
            try:
                sensor = self.module.methane()[1]
                lie = self.module.limit_value_meth()[1]
                message = self.module.message_meth()[1]
            except TypeError:
                pass
            else:
                if sensor > lie:
                    self.module.alarm.message(message)
                    self.module.meth_actuator(False)

