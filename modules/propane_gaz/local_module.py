import module
import fields.proxy
import fields.sensor
import fields.actuator
import fields.io
import fields.persistant
import fields.syntax

class PropaneGaz(module.Base):
    public_name = 'Propane'

    class propane(fields.sensor.Propane,
            fields.syntax.Percentage,
            fields.io.Graphable,
            fields.persistant.Database,
            fields.Base):
        public_name = 'Taux de propane (% dans l air)'

    class gaz_actuator(fields.actuator.Propane,
            fields.syntax.Boolean,
	    fields.io.Readable,
            fields.persistant.Volatile,
            fields.Base):
        public_name = 'Robinet de propane'
