from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class ActionneurAlarme(core.module.Base):
    update_rate = 10
    class Alarme(
            core.fields.actuator.Alarme,
            core.fields.io.Writable,
            core.fields.Base)
