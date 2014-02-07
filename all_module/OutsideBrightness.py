import module
import fields
import fields.io
import fields.sensor

class OutsideBrightness(module.Base):
    update_rate = 10

    class brightness(fields.sensor.Light, fields.io.Readable, fields.Base):
        pass
