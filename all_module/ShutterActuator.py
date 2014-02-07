from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class ShutterActuator(core.module.Base):	
    update_rate = 10
    class Shutter(
            core.fields.actuator.Shutter
            core.fields.io.Writable,
            core.fields.Base)
		