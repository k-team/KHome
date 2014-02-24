import module
import fields

class ButaneGaz(module.Base):
    public_name = 'Butane'

    class butane(fields.sensor.Butane, fields.syntax.Numeric,
            fields.io.Graphable, fields.persistant.Database, fields.Base):
        public_name = 'Taux de butane'

    class gaz_actuator(fields.actuator.Butane, fields.io.Readable,
            fields.syntax.Boolean, fields.persistant.Volatile, fields.Base):
        public_name = 'Robinet de butane'
