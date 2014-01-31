from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class TempActionneur(core.module.Base):
    update_rate = 10
    class Temperature(
        core.fields.actuator.Temperature,
        core.fields.io.Writable,
        core.fields.Base):
    pass
