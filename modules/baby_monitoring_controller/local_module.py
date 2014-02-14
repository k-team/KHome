import module
from module import use_module
import fields

class BabyMonitoringController(module.Base):
    update_rate = 10
    sound_sensor = use_module('SoundSensor')
    alarm_actuator = use_module('AlarmActuator')

    class controller(fields.Base):

        def __init__(self):
            self.decibel_value = 97 #seuil du cri d'un nourisson
            super(BabyMonitoringController.controller, self).__init__()
    
        def always(self):
            #print 'sound = %s' % self.module.sound_sensor.sound()[1]
            #print 'decibel_limit = %s' % self.decibel_value
            
            if self.module.sound_sensor.sound()[1] > self.decibel_value:
                self.module.alarm_actuator.alarm(True)
                #print 'alerte'
            else:
                self.module.alarm_actuator.alarm(False)
                #print 'pas alerte'
    
