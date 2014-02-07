import module
import fields
import fields.io
import fields.actuator

class DoorActuator(module.Base):
    update_rate = 10

    class Door(fields.actuator.Door, fields.io.Writable, fields.Base):
        pass

