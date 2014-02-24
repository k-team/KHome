import module
import fields

class SoundSensor(module.Base):
    update_rate = 2
    public_name = 'Capteur sonore'

    class sound(fields.syntax.Numeric, fields.sensor.Sound,
            fields.io.Graphable, fields.persistant.Database, fields.Base):
        public_name = 'Volume (db)'
