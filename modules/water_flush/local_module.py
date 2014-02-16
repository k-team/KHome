import module
import fields.proxy

class WaterFlush(module.Base):
    update_rate = 10
    flush = fields.proxy.mix('flush', 'HumanPresenceSensor', 'presence','PistonActuator', 'piston')
