from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class SoundSensor(core.module.Base):
    update_rate = 10
    class Sound(
        		core.fields.sensor.Sound
        		core.fields.io.Readable,
        		core.fields.Base):
    		pass