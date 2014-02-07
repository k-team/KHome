import module
import fields
import fields.io
import fields.actuator

class DoorActuator(module.Base):
    update_rate = 10

    class door(fields.actuator.Door, fields.io.Writable, fields.Base):
        pass
