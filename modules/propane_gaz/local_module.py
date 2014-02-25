import module
from module import use_module
import fields

class PropaneGaz(module.Base):
    update_rate = 1000
    public_name = 'Propane'

    alarm = use_module('Alarm')

    class propane(fields.sensor.Propane,
            fields.syntax.Numeric,
            fields.io.Graphable,
            fields.persistant.Database,
            fields.Base):
        update_rate = 60
        public_name = 'Taux de propane (% dans l\'air)'

    class limit_value_prop(
            fields.syntax.Numeric,
            fields.io.Readable,
            fields.persistant.Database,
            fields.Base):
        public_name = 'LIE Propane'
        init_value = 2.10

    class message_prop(
            fields.syntax.String,
            fields.io.Readable,
            fields.io.Writable,
            fields.persistant.Database,
            fields.Base):
        public_name = 'Message d\'alerte propane'
        init_value = 'Au #secours il y a la masse de #propane #YOLO'

    class prop_actuator(fields.actuator.Propane, fields.syntax.Boolean,
            fields.io.Readable, fields.persistant.Volatile, fields.Base):
        public_name = 'Vanne de propane'

    class security(fields.Base):
        update_rate = 60

        def always(self):
            try:
                sensor = self.module.propane()[1]
                lie = self.module.limit_value_prop()[1]
                message = self.module.message_prop()[1]
            except TypeError:
                pass
            else:
                if sensor > lie:
                    self.module.alarm.message(message)
                    self.module.prop_actuator(False)
