from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class CapteurCO(core.module.Base):
    update_rate = 10
    class PresenceCO(
            core.fields.sensor.PresenceCO,
            core.fields.io.Readable,
            core.fields.Base):
        pass
