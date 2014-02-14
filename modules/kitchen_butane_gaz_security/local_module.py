import module
import fields.proxy

class KitchenButaneGazSecurity(module.Base):
    update_rate = 10

    alarm = fields.proxy.writable('alarm', 'AlarmActuator', 'alarm')
    gaz = fields.proxy.mix('gaz', 'ButaneSensor', 'butane_presence',
            'GazActuator', 'gaz')
