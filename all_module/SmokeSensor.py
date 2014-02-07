import module
import fields
import fields.io
import fields.sensor

class SmokeSensor(module.Base):
    update_rate = 10

    class smoke(fields.sensor.Smoke, fields.io.Readable, fields.Base):
        pass
