import module
import fields
import fields.io
import fields.sensor
import fields.persistant

class RainForecast(module.Base):
    update_rate = 10

    class rain(fields.sensor.RainForecast, fields.io.Readable, fields.persistant.Volatile, fields.Base):
        pass
