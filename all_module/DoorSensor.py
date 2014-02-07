from twisted.internet import reactor
import module
import fields
import fields.io
import fields.persistant
import time

class DoorSensor(module.Base):
    update_rate = 10
    class Door(
            fields.sensor.Door
            fields.io.Readable,
            fields.Base):
        pass

