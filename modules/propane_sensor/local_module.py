import module
import fields
import fields.io
import fields.sensor
import fields.persistant
import fields.syntax

class PropaneSensor(module.Base):
    update_rate = 10

    class propane_presence(fields.syntax.Numeric, fields.sensor.Propane, fields.io.Readable,  fields.persistant.Volatile, fields.Base):
        pass
