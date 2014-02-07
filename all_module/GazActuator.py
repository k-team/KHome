import module
import fields
import fields.io
import fields.actuator

class GazActuator(module.Base):
    update_rate = 10

    class gaz(fields.actuator.Gaz, fields.io.Writable, fields.Base):
        pass
