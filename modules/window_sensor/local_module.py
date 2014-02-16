import module
import fields
import fields.sensor
import fields.io
import fields.persistant
import fields.syntax

class WindowSensor(module.Base):
    update_rate = 10

    class window(fields.syntax.Boolean, fields.sensor.WindowsContact, fields.io.Readable, fields.persistant.Volatile, fields.Base):
        pass
