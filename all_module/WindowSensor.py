import module
import fields
import fields.io
import fields.persistant

class WindowSensor(module.Base):
    update_rate = 10

    class Window(fields.sensor.Window, fields.io.Readable, fields.Base):
        pass
