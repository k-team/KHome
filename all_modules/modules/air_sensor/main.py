from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class AirSensor(core.module.Base):
    update_rate = 10
    class Air(
            core.fields.sensor.Air,
            core.fields.io.Readable,
            core.fields.Base):
        pass
