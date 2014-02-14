from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class MoistureSensor(module.Base):
    update_rate = 10
    class moisture(
            fields.sensor.Moisture,
            fields.io.Readable,
            fields.Base):
        pass
