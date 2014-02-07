from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class LightSensor(core.module.Base):
    update_rate = 10
    class LightButton(
            core.fields.sensor.LightInterruptor
            core.fields.io.Readable,
            core.fields.persistant.Volatile,
            core.fields.Base):
        pass
        