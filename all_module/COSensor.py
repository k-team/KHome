from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class COSensor(core.module.Base):
    update_rate = 10
    class COPresence(
            core.fields.sensor.COPresence,
            core.fields.io.Readable,
            core.fields.Base):
        pass
