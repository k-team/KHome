import module
import fields
import fields.io
import fields.sensor

class TemperatureForecast(module.Base):
    update_rate = 10

    class temperature(fields.sensor.TemperatureForecast, fields.io.Readable,
            fields.Base):
        pass
