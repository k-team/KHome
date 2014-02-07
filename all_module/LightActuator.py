from twisted.internet import reactor
import module
import fields
import fields.io
import fields.persistant
import time

class LightActuator(module.Base):
	update_rate = 10
    class LightButton(
            fields.actuator.LightInterruptor
            fields.io.Writable,
            fields.Base)

