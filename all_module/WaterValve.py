from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class WaterValveSensor(core.module.Base):
    update_rate = 10
    class WaterValve(
            core.fields.sensor.WaterValve,
            core.fields.io.Readable,
            core.fields.Base):
        pass
