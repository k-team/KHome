import module
import fields.proxy

class Shutter(module.Base):
    update_rate = 10

    class shutter(fields.sensor.Shutter, fields.actuator.Shutter,
            fields.persistant.Volatile, fields.Base):
        pass
