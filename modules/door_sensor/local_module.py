import module
import fields
import fields.io
import fields.sensor
import fields.persistant

class DoorSensor(module.Base):
    update_rate = 10

    class door(fields.sensor.WindowsContact, fields.io.Readable, fields.persistant.Volatile, fields.Base):
        pass
        
    

