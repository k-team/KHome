import module
import fields.proxy
import fields.sensor
import fields.actuator
import fields.io
import fields.persistant
import fields.syntax

class ButaneGaz(module.Base):
    public_name = 'Butane'

    class butane(fields.sensor.Butane,
            fields.syntax.Percentage,
            fields.io.Graphable,
            fields.persistant.Database,
            fields.Base):
        public_name = 'Taux de butane (% dans l air)'

    class gaz_actuator(fields.actuator.Butane,
            fields.io.Readable,
            fields.syntax.Boolean,
            fields.persistant.Volatile,
            fields.Base):
        public_name = 'Robinet de butane'
