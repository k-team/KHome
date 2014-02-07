import module
import fields.proxy

class KitchenPropaneGazSecurity(module.Base):
    update_rate = 10

    alarm = fields.proxy.writable('Alarm', 'AlarmActuator', 'Alarm')
    gaz = fields.proxy.mix('Gaz', 'PropaneSensor', 'PropanePresence',
            'GazActuator', 'Gaz')
