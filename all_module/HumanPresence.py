import module
import fields
import fields.io
import fields.sensor

class HumanPresence(module.Base):
    update_rate = 10

    class presence(fields.sensor.Presence, fields.io.Readable, fields.Base):
        pass
