import module
import fields
import fields.io
import fields.sensor
import fields.persistant
import fields.syntax

class MoistureSensor(module.Base):
    update_rate = 10

    class moisture(fields.syntax.Numeric, fields.sensor.Moisture,
            fields.io.Readable, fields.persistant.Volatile, fields.Base):
        pass
