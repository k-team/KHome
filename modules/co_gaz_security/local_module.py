import module
import fields.proxy

class COGazSecurity(module.Base):
    update_rate = 10

    gaz = fields.proxy.mix('gaz', 'COSensor', 'co_presence', 'AlarmActuator',
            'alarm')
