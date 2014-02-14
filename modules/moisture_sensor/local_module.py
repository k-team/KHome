import module
import fields
import fields.io
import fields.sensor
import fields.persistant

class MoistureSensor(module.Base):
    update_rate = 10
    
    class moisture(
            fields.sensor.Moisture,
            fields.io.Readable,
            fields.persistant.Volatile,
            fields.Base):
        pass
