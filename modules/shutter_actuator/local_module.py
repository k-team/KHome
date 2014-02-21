import module
import fields
import fields.io
import fields.actuator
import fields.persistant
import fields.syntax

class ShutterActuator(module.Base):
    update_rate = 10

    class shutter(fields.actuator.Shutter, fields.Base):
        pass
