import module
from module import use_module
import fields

class ButaneGaz(module.Base):
    update_rate = 1000
    public_name = 'Butane'

    alarm = use_module('Alarm')

    class butane(fields.sensor.Butane,
            fields.syntax.Numeric,
            fields.io.Graphable,
            fields.persistant.Database,
            fields.Base):
        update_rate = 60
        public_name = 'Taux de butane (% dans l\'air)'

    class limit_value_but(
            fields.syntax.Numeric,
            fields.io.Readable,
            fields.persistant.Database,
            fields.Base):
        public_name = 'LIE Butane'
        init_value = 1.80

    class message_but(
            fields.syntax.String,
            fields.io.Readable,
            fields.io.Writable,
            fields.persistant.Database,
            fields.Base):
        public_name = 'Message d\'alerte butane'
        init_value = 'Au #secours il y a la masse de #butane #YOLO'

    class but_actuator(fields.actuator.Butane, fields.syntax.Boolean,
            fields.io.Readable, fields.persistant.Volatile, fields.Base):
        public_name = 'Vanne de butane'

    class security(fields.Base):
        update_rate = 60

        def always(self):
            try:
                sensor = self.module.butane()[1]
                lie = self.module.limit_value_but()[1]
                message = self.module.message_but()[1]
            except TypeError:
                pass
            else:
                if sensor > lie:
                    self.module.alarm.message(message)

