import module
import fields
import fields.io
import fields.sensor
import fields.persistant
import fields.syntax

class ShutterSensor(module.Base):
    update_rate = 10

    class shutter(
            fields.syntax.Numeric, 
            fields.sensor.Shutter, 
            fields.io.Readable, 
            fields.persistant.Volatile, 
            fields.Base):
        pass
