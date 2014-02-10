import module
import fields
import fields.io
import fields.actuator

class PistonActuator(module.Base):
    update_rate = 10

    class piston(fields.actuator.Piston, fields.io.Writable, fields.Base):
        pass
