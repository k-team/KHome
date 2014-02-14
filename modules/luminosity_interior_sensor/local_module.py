import module
import fields
import fields.io
import fields.sensor
import fields.persistant

class LuminosityInteriorSensor(module.Base):
    update_rate = 10

    
    class luminosity(
            fields.sensor.LuminosityInterior,
            fields.io.Readable,
            fields.persistant.Volatile,
            fields.Base):
        pass
        
    
