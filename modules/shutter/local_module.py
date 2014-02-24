import module
import fields
import fields.io
import fields.syntax
import fields.sensor
import fields.actuator
import fields.persistant

class Shutter(module.Base):
    update_rate = 10
    public_name = 'Volets'

    class shutter(fields.actuator.Shutter, fields.sensor.Shutter,
            fields.persistant.Volatile, fields.Base):
        public_name = 'Position des volets'
