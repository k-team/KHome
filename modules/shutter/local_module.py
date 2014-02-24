import module
import fields

class Shutter(module.Base):
    update_rate = 10

    class shutter(fields.actuator.Shutter, fields.sensor.Shutter,
            fields.persistant.Volatile, fields.Base):
        public_name = 'Position des volets'
