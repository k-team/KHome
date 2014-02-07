from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class PropaneSensor (core.module.Base):
    update_rate = 10
    class PropanePresence(
            core.fields.sensor.PropanePresence,
            core.fields.io.Readable,
            core.fields.Base):
        pass
