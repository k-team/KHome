import module
import fields
import fields.io
import fields.sensor
import fields.syntax
import fields.persistant

class CameraSensor(module.Base):
    update_rate = 10

    class image(fields.syntax.Numeric,
            fields.sensor.Camera,
            fields.persistant.Volatile,
            fields.io.Readable,
            fields.Base):
        pass
