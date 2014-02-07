from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class SmokeSensor(core.module.Base):
    update_rate = 10
    class Smoke(
		        core.fields.sensor.Smoke
		        core.fields.io.Readable,
		        core.fields.Base):
		    pass
