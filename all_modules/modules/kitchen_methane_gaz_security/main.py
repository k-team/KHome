import module
import fields.proxy

class KitchenMethaneGazSecurity(module.Base):
    update_rate = 10

    alarm = fields.proxy.writable('Alarm', 'AlarmActuator', 'Alarm')
    gaz = fields.proxy.mix('Gaz', 'MethaneSensor', 'MethanePresence',
            'GazActuator', 'Gaz')
