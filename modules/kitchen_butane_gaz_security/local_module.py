import module
import fields.proxy

class KitchenButaneGazSecurity(module.Base):
    update_rate = 10
    taux = fields.proxy.readable('taux', 'ButaneSensor', 'butane_presence')
    alarm = fields.proxy.writable('alarm', 'AlarmActuator', 'alarm')
    gaz_actuator = fields.proxy.writable('gaz_actuator', 'GazActuator', 'gaz')
    #gaz = fields.proxy.mix('gaz', 'ButaneSensor', 'butane_presence',
    #        'GazActuator', 'gaz')
