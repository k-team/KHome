from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class DoorActuator(core.module.Base):
    update_rate = 10
    class Door(
            core.fields.actuator.Door
            core.fields.io.Writable,
            core.fields.Base)
    