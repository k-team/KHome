import module
import fields.proxy
import fields.sensor
import fields.actuator
import fields.io
import fields.persistant
import fields.syntax

class PropaneGaz(module.Base):

    class taux(fields.sensor.Propane,
            fields.syntax.Numeric,
            fields.io.Graphable,
            fields.persistant.Database,
            fields.Base):
        public_name = 'Taux de propane'

    class gaz_actuator(fields.actuator.Propane,
            fields.syntax.Boolean,
	    fields.io.Readable,
            fields.persistant.Volatile,
            fields.Base):
        public_name = 'Robinet de propane'