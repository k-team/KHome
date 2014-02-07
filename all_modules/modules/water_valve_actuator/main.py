from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class WaterValveActuator(core.module.Base):
    update_rate = 10
    class WaterValve(
            core.fields.actuator.WaterValve,
            core.fields.io.Writable,
            core.fields.Base)
