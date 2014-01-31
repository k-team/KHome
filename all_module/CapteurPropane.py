from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class CapteurPropane (core.module.Base):
    update_rate = 10
    class PresencePropane(
            core.fields.sensor.PresencePropane,
            core.fields.io.Readable,
            core.fields.Base):
        pass
