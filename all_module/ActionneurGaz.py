from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class ActionneurGaz(core.module.Base):
    update_rate = 10
    class Gaz(
            core.fields.actuator.Gaz,
            core.fields.io.Writable,
            core.fields.Base)
