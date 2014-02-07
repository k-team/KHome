from twisted.internet import reactor
import module
import fields
import fields.io
import fields.persistant
import time

class COGazSecurity(module.Base):
    update_rate = 10
    Gaz = fields.proxy.mix('Gaz',
                           'COSensor', 'COPresence',
                           'AlarmActuator', 'Alarm')
