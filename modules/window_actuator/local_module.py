import module
import fields
import fields.io
import fields.actuator

class WindowActuator(module.Base):
    update_rate = 10

    class window(fields.actuator.Window, fields.io.Writable, fields.Base):
        pass
