import module
import fields
import fields.io
import fields.actuator

class ElectricCurrentActuator(module.Base):
    update_rate = 10

    class electric_current(fields.actuator.ElectricCurrent, fields.io.Writable,
            fields.Base):
        pass

