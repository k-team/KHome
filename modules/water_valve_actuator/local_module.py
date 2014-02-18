import module
import fields
import fields.actuator
import fields.io

class WaterValveActuator(module.Base):
    update_rate = 10
    class water_valve(
            fields.actuator.WaterValve,
            fields.io.Writable,
            fields.Base):
                pass
