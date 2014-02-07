from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time
import all_modules.SoundSensor
import all_modules.AlarmActuator

class BabyMonitoringController(core.module.Base)
    update_rate = 10
    sound_sensor = use_module('SoundSensor')
    alarm_actuator = use_module('AlarmActuator')

    class Controller(
        core.fields.Base):

        def _init_:
            DECIBEL_VALUE = 100
            super(Controller, self)._init_
        
        def always(self):
            if sound_sensor.Sound() > DECIBEL_VALUE:
                alarm_actuator.Alarm(true)
            else
                alarm_actuator.Alarm(false)
    
