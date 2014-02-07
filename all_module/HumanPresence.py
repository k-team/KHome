from twisted.internet import reactor
import module
import fields
import fields.io
import fields.persistant
import time

class HumanPresence(module.Base):
    update_rate = 10
    class Presence(
            fields.sensor.Presence,
            fields.io.Readable,
            fields.Base):
        pass
