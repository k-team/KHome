from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class KitchenPropaneGazSecurity(core.module.Base):
    update_rate = 10
    Alarm = fields.proxy.writable('Alarm', 
    															'AlarmActuator', 'Alarm')
    Gaz = fields.proxy.mix('Gaz',
                           'PropaneSensor', 'PropanePresence',
                           'GazActuator', 'Gaz')
