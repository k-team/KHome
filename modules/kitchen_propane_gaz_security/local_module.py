import module
import fields.proxy

class KitchenPropaneGazSecurity(module.Base):
    update_rate = 10

    alarm = fields.proxy.writable('alarm', 'AlarmActuator', 'alarm')
    taux = fields.proxy.readable('taux', 'PropaneSensor', 'propane_presence')
    gaz_actuator = fields.proxy.writable('gaz_actuator', 'GazActuator', 'gaz')
    #gaz = fields.proxy.mix('gaz', 'PropaneSensor', 'propane_presence',
      #      'GazActuator', 'gaz')
