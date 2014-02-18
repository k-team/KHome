import module
import fields
import fields.io
import fields.sensor
import fields.persistant
import fields.syntax

class TemperatureExteriorSensor(module.Base):
    update_rate = 10
    
    class temperature(
            fields.syntax.Numeric,
            fields.sensor.TemperatureExterior,
            fields.io.Readable,
            fields.persistant.Volatile,
            fields.Base):
        pass
