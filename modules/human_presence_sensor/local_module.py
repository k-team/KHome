import module
import fields
import fields.io
import fields.sensor
import fields.persistant

class HumanPresenceSensor(module.Base):
    update_rate = 10

    class presence(fields.sensor.Presence, fields.io.Readable, fields.persistant.Volatile, fields.Base):
        pass
