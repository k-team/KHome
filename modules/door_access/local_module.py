import module
import fields
import fields.actuator
import fields.sensor
import fields.persistant

class DoorAccess(module.Base):
    update_rate = 10

    class door(fields.sensor.Contact, fields.actuator.Door,
            fields.persistant.Volatile, fields.Base):
        pass
