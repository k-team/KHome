from twisted.internet import reactor
import time
import module
import fields
import fields.io
import fields.persistant

class BabyMonitoring(module.Base):
    update_rate = 10
    soundSensor = use_module('SoundSensor')
    recognition = use_module('Recognition')
    alarmActuator = use_module('AlarmActuator')

    Baby = fields.proxy.mix('Baby', 'SoundSensor', 'Sound', 'Recognition',
            'Recognised', 'AlarmActuator', 'Alarm')
