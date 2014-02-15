import module
import fields
import fields.io
import fields.sensor
import fields.persistant

class AirSensor(module.Base):
    update_rate = 10
    class air(
            fields.sensor.Air,
            fields.io.Readable,
            fields.persistant.Volatile,
            fields.Base):
        pass
    
    def always(self):
        print 'ceci est un petit test'
