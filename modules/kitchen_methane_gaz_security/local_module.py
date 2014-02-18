import module
import fields.proxy

class KitchenMethaneGazSecurity(module.Base):
    update_rate = 10

    alarm = fields.proxy.writable('alarm', 'AlarmActuator', 'alarm')
    taux = fields.proxy.readable('taux', 'MethaneSensor', 'methane_presence')
    gaz_actuator = fields.proxy.writable('gaz_actuator', 'GazActuator', 'gaz')
