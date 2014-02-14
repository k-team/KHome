import module
from module import use_module
import fields

class BabyMonitoringController(module.Base):
    update_rate = 10
    sound_sensor = use_module('SoundSensor')
    alarm_actuator = use_module('AlarmActuator')

    class controller(fields.Base):

        def _init_:
            decibel_value = 97 #seuil du cri d'un nourisson
            super(BabyMonitoringController.controller, self)._init_
        
        def always(self):
            if self.module.sound_sensor.sound() > self.module.decibel_value:
                self.module.alarm_actuator.alarm(True)
            else:
                self.module.alarm_actuator.alarm(False)
    
