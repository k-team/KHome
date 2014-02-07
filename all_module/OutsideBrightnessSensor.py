from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class OutsideBrightness(core.module.Base):
    update_rate = 10
    class Brightness(
            core.fields.sensor.Light,
            core.fields.io.Readable,
            core.fields.Base):
        pass
