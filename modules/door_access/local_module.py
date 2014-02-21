import module
import fields.io
import fields.actuator
import fields.sensor
import fields.persistant
import fields.syntax


class DoorAccess(module.Base):
    update_rate = 10
    
    class door(#fields.syntax.Boolean,
            fields.sensor.Contact,
            fields.actuator.Door,
            fields.persistant.Volatile,
            fields.Base):
        pass        
    
    
