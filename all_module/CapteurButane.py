from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class CapteurButane (core.module.Base):
    update_rate = 10
    class PresenceButane(
            core.fields.sensor.PresenceButane,
            core.fields.io.Readable,
            core.fields.Base):
        pass
