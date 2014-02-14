import module
import fields
import fields.io
import fields.sensor
import fields.persistant

class TemperatureForecast(module.Base):
    update_rate = 10

    class temperature(fields.sensor.TemperatureForecast,
            fields.persistant.Volatile,
            fields.io.Readable,
            fields.Base):
        pass
