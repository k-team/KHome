import module
import fields
import fields.io
import fields.sensor

class CameraSensor(module.Base):
    update_rate = 10

    class image(fields.sensor.Camera, fields.io.Readable, fields.Base):
        pass
