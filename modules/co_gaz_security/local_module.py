import module
import fields.proxy

class COGazSecurity(module.Base):
    update_rate = 10
    taux = fields.proxy.readable('taux', 'COSensor', 'co_presence')
    alarm = fields.proxy.writable('alarm', 'AlarmActuator', 'alarm')
    #gaz = fields.proxy.mix('gaz', 'COSensor', 'co_presence', 'AlarmActuator',
    #        'alarm')
