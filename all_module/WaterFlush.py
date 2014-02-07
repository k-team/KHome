from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class WaterFlush(core.module.Base):
    Flush = fields.proxy.mix('Flush', 
                                'ActuatorPiston', 'Piston', 
                                'HumanPresenceSensor', 'Presence')
