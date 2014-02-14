import module
import fields.proxy

class KitchenMethaneGazSecurity(module.Base):
    update_rate = 10

    alarm = fields.proxy.writable('alarm', 'AlarmActuator', 'alarm')
    gaz = fields.proxy.mix('gaz', 'MethaneSensor', 'methane_presence',
            'GazActuator', 'gaz')
