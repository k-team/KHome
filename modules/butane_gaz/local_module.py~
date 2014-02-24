import module
import fields.proxy
import fields.sensor
import fields.actuator
import fields.io
import fields.persistant
import fields.syntax

class ButaneGaz(module.Base):

    class taux(fields.sensor.Butane,
            fields.syntax.Numeric,
            fields.io.Graphable,
            fields.persistant.Database,
            fields.Base):
        public_name = 'Taux de butane'

    class gaz_actuator(fields.actuator.Butane,
            fields.io.Readable,
            fields.syntax.Boolean,
            fields.persistant.Volatile,
            fields.Base):
        public_name = 'Robinet de butane'
