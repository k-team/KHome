from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class CapteurCamera(core.module.Base):
    update_rate = 10
    class Image(
            core.fields.sensor.Camera,
            core.fields.io.Readable,
            core.fields.Base)
