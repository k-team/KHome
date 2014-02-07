from twisted.internet import reactor
import module
import fields
import fields.io
import fields.persistant
import time

class KitchenPropaneGazSecurity(module.Base):
    update_rate = 10
    Alarm = fields.proxy.writable('Alarm',
    															'AlarmActuator', 'Alarm')
    Gaz = fields.proxy.mix('Gaz',
                           'PropaneSensor', 'PropanePresence',
                           'GazActuator', 'Gaz')
