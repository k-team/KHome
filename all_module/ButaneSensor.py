from twisted.internet import reactor
import module
import fields
import fields.io
import fields.persistant
import time

class ButaneSensor (module.Base):
    update_rate = 10
    class ButanePresence(
            fields.sensor.ButanePresence,
            fields.io.Readable,
            fields.Base):
        pass
