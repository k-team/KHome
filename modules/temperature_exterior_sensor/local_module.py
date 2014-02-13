import module
import fields
import fields.io
import fields.persistant
import fields.sensor

class TemperatureExteriorSensor(module.Base):
    update_rate = 10
    
    class Temperature(
            fields.sensor.TemperatureExterior
            fields.io.Readable,
            fields.persistant.Volatile,
            fields.Base):
        pass