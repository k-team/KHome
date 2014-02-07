from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class FanActuator(core.module.Base):
    update_rate = 10
    class Fan(
            core.fields.actuator.Fan,
            core.fields.io.Writable,
            core.fields.Base)
