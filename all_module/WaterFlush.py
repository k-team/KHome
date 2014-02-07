from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class WaterFlush(core.module.Base):
    update_rate = 10
    pistonActuator = use_module('ActuatorPiston')
    humanPresence = use_module('HumanPresenceSensor')

    Flush = fields.proxy.mix('Flush',
    												 'ActuatorPiston', 'Piston', 
    												 'HumanPresenceSensor', 'Presence')
