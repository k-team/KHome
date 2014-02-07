from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class BabyMonitoring(core.module.Base):
    update_rate = 10
    soundSensor = use_module('SoundSensor')
    recognition = use_module('Recognition')
    alarmActuator = use_module('AlarmActuator')

    Baby = fields.proxy.mix('Baby',
    												'SoundSensor', 'Sound', 
    												'Recognition', 'Recognised', 
    												'AlarmActuator', 'Alarm')
    