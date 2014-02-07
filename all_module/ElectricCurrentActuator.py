from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class ElectricCurrentActuator(core.module.Base):
    update_rate = 10
    class ElectricCurrent(
            core.fields.actuator.ElectricCurrent
            core.fields.io.Writable,
            core.fields.Base)
    