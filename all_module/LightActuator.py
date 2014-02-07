from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class LightActuator(core.module.Base):
	update_rate = 10
    class LightButton(
            core.fields.actuator.LightInterruptor
            core.fields.io.Writable,
            core.fields.Base)
		