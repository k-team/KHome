import module
from module import use_module
import fields.proxy

class WaterFlush(Base):
    update_rate = 10

    flush = fields.proxy.mix('Flush', 'ActuatorPiston', 'Piston',
            'HumanPresenceSensor', 'Presence')
