import module
import fields
import fields.io
import fields.sensor
import fields.persistant
import fields.syntax

class SoundSensor(module.Base):
    update_rate = 10
    public_name = 'Capteur de son'

    class sound(fields.syntax.Numeric, fields.sensor.Sound, fields.io.Readable, fields.persistant.Volatile, fields.Base):
        pass
