import module
import fields
import fields.io
import fields.sensor
import fields.persistant
import fields.syntax

class SoundSensor(module.Base):
    update_rate = 2
    public_name = 'Capteur sonore'

    class sound(fields.syntax.Numeric,
            fields.sensor.Sound,
            # fields.io.Readable,
            fields.io.Graphable,
            fields.persistant.Database,
            fields.Base):
        public_name = 'Volume (db)'
