import module
import fields
import fields.io
import fields.sensor
import fields.persistant

class COSensor(module.Base):
    update_rate = 10

    class co_presence(fields.sensor.CO, fields.io.Readable,
    fields.persistant.Volatile,
            fields.Base):
        pass
