import module
import fields
import fields.io
import fields.sensor
import fields.persistant
import fields.syntax

class RainForecast(module.Base):
    update_rate = 10

    class rain(fields.syntax.Boolean, fields.sensor.RainForecast, fields.io.Readable, fields.persistant.Volatile, fields.Base):
        pass
