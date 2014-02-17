import module
import fields
import fields.io
import fields.actuator

class TemperatureActuator(module.Base):
    update_rate = 10

    class temperature(
            fields.actuator.Temperature,
            fields.Base):
        pass
