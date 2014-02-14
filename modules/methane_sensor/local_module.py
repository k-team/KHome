import module
import fields
import fields.io
import fields.sensor
import fields.persistant


class MethaneSensor(module.Base):
    update_rate = 10

    class methane_presence(fields.sensor.Methane, fields.io.Readable,  fields.persistant.Volatile, fields.Base):
        pass
