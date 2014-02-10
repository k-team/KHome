import module
import fields.proxy

class KitchenButaneGazSecurity(module.Base):
    update_rate = 10

    alarm = fields.proxy.writable('Alarm', 'AlarmActuator', 'Alarm')
    gaz = fields.proxy.mix('Gaz', 'ButaneSensor', 'ButanePresence',
            'GazActuator', 'Gaz')
