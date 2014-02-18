import module
import fields
import fields.io
import fields.sensor
import fields.persistant
import fields.syntax

class SmokeSensor(module.Base):
    update_rate = 10

    class smoke(fields.syntax.Numeric, fields.sensor.Smoke, fields.io.Readable,  fields.persistant.Volatile, fields.Base):
        pass
