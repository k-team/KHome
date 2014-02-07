from twisted.internet import reactor
import module
import fields
import fields.io
import fields.persistant
import time

class CameraSensor(module.Base):
    update_rate = 10
    class Image(
            fields.sensor.Camera,
            fields.io.Readable,
            fields.Base)
