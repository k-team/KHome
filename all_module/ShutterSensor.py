import module
import fields
import fields.io
import fields.sensor
import fields.persistant

class ShutterSensor(module.Base):
    update_rate = 10

    class shutter(fields.sensor.Shutter, fields.io.Readable, fields.persistant.Volatile, fields.Base):
        pass
