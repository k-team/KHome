import module
import fields
import fields.io
import fields.actuator

class FanActuator(module.Base):
    update_rate = 10
    class fan(
            fields.actuator.Fan,
            fields.io.Writable,
            fields.Base):
        pass
