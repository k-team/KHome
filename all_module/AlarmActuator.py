from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class AlarmActuator(core.module.Base):
    update_rate = 10
    class Alarm(
            core.fields.actuator.Alarm,
            core.fields.io.Writable,
            core.fields.Base)
