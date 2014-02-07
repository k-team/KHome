from twisted.internet import reactor
import module
import fields
import fields.io
import fields.persistant
import time

class ElectricCurrentSensor(module.Base):
    update_rate = 10
    class ElectricCurrent(
            fields.sensor.ElectricCurrent
            fields.io.Readable,
            fields.persistant.Volatile,
            fields.Base):
        pass

