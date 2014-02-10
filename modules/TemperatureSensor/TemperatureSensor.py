import module
import fields
import fields.io
import fields.sensor

class TemperatureSensor(module.Base):
    update_rate = 10

    class temperature(fields.sensor.Temperature, fields.io.Readable,
            fields.Base):
        pass
