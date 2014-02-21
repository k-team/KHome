import module
import fields
import fields.io
import fields.sensor
import fields.persistant
import fields.syntax

class HumanPresenceSensor(module.Base):
    update_rate = 1
    public_name = 'Capteur de presence'

    class presence(fields.syntax.Boolean, fields.sensor.Presence, fields.io.Readable, fields.persistant.Volatile, fields.Base):
        pass
