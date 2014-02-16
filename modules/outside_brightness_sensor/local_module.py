import module
import fields
import fields.io
import fields.sensor
import fields.persistant

class OutsideBrightness(module.Base):
    update_rate = 10

    class brightness(fields.sensor.LuminosityExterior,
            fields.io.Readable,
            fields.persistant.Volatile,
            fields.Base):
        pass
