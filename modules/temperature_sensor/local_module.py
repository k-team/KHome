import module
import fields
import fields.io
import fields.sensor
import fields.persistant

class TemperatureSensor(module.Base):
    update_rate = 10

    class temperature(fields.sensor.Temperature, fields.io.Readable,  fields.persistant.Volatile,
            fields.Base):
        pass
