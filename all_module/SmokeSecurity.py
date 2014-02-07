from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class SmokeSecurity(core.module.Base):
    update_rate = 10
    alarmActuator = use_module('AlarmActuator')

    Security = fields.proxy.mix('Security',
								'SmokeSensor','Smoke',
								'AlarmActuator', 'Alarm')
