import module
import fields
import fields.io
import fields.sensor

class COSensor(module.Base):
    update_rate = 10

    class co_presence(fields.sensor.COPresence, fields.io.Readable,
            fields.Base):
        pass
