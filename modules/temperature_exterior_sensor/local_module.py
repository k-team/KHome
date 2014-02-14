import module
import fields
import fields.io
import fields.sensor
import fields.persistant

class TemperatureExteriorSensor(module.Base):
    update_rate = 10
    
    class temperature(
            fields.sensor.TemperatureExterior,
            fields.io.Readable,
            fields.persistant.Volatile,
            fields.Base):
        pass
