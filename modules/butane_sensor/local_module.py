import module
import fields
import fields.io
import fields.sensor
import fields.persistant
import fields.syntax

class ButaneSensor (module.Base):
    update_rate = 10
    public_name = 'Capteur de butane'

    class butane_presence(fields.sensor.Butane,
            fields.syntax.Numeric,
	    fields.io.Readable,
            fields.persistant.Volatile,
            fields.Base):
        pass
