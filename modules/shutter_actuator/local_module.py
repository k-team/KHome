import module
import fields
import fields.io
import fields.actuator
import fields.persistant

class ShutterActuator(module.Base):
    update_rate = 10

    class shutter(fields.actuator.Shutter, fields.io.Writable, fields.Base):
        pass