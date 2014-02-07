from twisted.internet import reactor
import module
import fields
import fields.io
import fields.persistant
import time

class GazActuator(module.Base):
    update_rate = 10
    class Gaz(
            fields.actuator.Gaz,
            fields.io.Writable,
            fields.Base)
