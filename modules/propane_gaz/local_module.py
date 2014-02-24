import module
import fields

class PropaneGaz(module.Base):
    public_name = 'Propane'

    class propane(fields.sensor.Propane,
            fields.syntax.Numeric,
            fields.io.Graphable,
            fields.persistant.Database,
            fields.Base):
        public_name = 'Taux de propane'

    class gaz_actuator(fields.actuator.Propane, fields.syntax.Boolean,
            fields.io.Readable, fields.persistant.Volatile, fields.Base):
        public_name = 'Robinet de propane'
