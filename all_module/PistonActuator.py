from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class PistonActuator(core.module.Base):
    update_rate = 10
    class Piston(
            core.fields.actuator.Piston,
            core.fields.io.Writable,
            core.fields.Base):
        pass
