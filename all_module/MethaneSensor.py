import module
import fields
import fields.io
import fields.sensor

class MethaneSensor(module.Base):
    update_rate = 10

    class methane_presence(fields.sensor.MethanePresence, fields.io.Readable, fields.Base):
        pass
