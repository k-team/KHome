from twisted.internet import reactor
import module
import fields
import fields.io
import fields.persistant
import time

class ElectricCurrentActuator(module.Base):
    update_rate = 10
    class ElectricCurrent(
            fields.actuator.ElectricCurrent
            fields.io.Writable,
            fields.Base)

