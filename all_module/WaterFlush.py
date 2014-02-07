import module
from module import use_module
import fields.proxy

class WaterFlush(Base):
    update_rate = 10

    PistonActuator = use_module('ActuatorPiston')
    HumanPresence = use_module('HumanPresence')

    flush = fields.proxy.mix('Flush', 'ActuatorPiston', 'Piston',
            'HumanPresence', 'Presence')
