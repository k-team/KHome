from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class ButaneSensor (core.module.Base):
    update_rate = 10
    class ButanePresence(
            core.fields.sensor.ButanePresence,
            core.fields.io.Readable,
            core.fields.Base):
        pass
