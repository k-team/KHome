from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class CapteurMethane(core.module.Base):
    update_rate = 10
    class PresenceMethane(
            core.fields.sensor.PresenceMethane,
            core.fields.io.Readable,
            core.fields.Base):
        pass
