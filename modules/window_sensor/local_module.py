import module
import fields
import fields.sensor
import fields.io
import fields.persistant

class WindowSensor(module.Base):
    update_rate = 10

    class window(fields.sensor.Window, fields.io.Readable, fields.persistant.Volatile, fields.Base):
        pass
