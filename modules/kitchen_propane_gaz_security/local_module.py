import module
import fields.proxy

class KitchenPropaneGazSecurity(module.Base):
    update_rate = 10

    alarm = fields.proxy.writable('alarm', 'AlarmActuator', 'alarm')
    gaz = fields.proxy.mix('gaz', 'PropaneSensor', 'propane_presence',
            'GazActuator', 'gaz')
