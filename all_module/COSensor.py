from twisted.internet import reactor
import module
import fields
import fields.io
import fields.persistant
import time

class COSensor(module.Base):
    update_rate = 10
    class COPresence(
            fields.sensor.COPresence,
            fields.io.Readable,
            fields.Base):
        pass
