import module
import fields.proxy

class COGazSecurity(module.Base):
    update_rate = 10

    gaz = fields.proxy.mix('Gaz', 'COSensor', 'COPresence', 'AlarmActuator',
            'Alarm')
