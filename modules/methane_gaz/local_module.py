import module
import fields.proxy
import fields.sensor
import fields.actuator
import fields.io
import fields.persistant
import fields.syntax

class MethaneGaz(module.Base):

    class methane(fields.sensor.Methane,
            fields.syntax.Numeric,
            fields.io.Graphable,
            fields.persistant.Database,
            fields.Base):
        public_name = 'Taux de methane'

    class gaz_actuator(fields.actuator.Methane,
            fields.syntax.Boolean,
	    fields.io.Readable,
            fields.persistant.Volatile,
            fields.Base):
        public_name = 'Robinet de methane'
