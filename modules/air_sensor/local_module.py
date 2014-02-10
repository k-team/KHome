import module
import fields
import fields.io
import fields.sensor
import fields.persistant
import time

class AirSensor(module.Base):
    update_rate = 10
    class Air(
            fields.sensor.Air,
            fields.io.Readable,
            fields.Base):
        pass
