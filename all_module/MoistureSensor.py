from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class MoistureSensor(core.module.Base):
    update_rate = 10
    class Moisture(
            core.fields.sensor.Moisture,
            core.fields.io.Readable,
            core.fields.Base):
        pass
