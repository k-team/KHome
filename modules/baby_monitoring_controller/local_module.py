import module
from module import use_module
import fields
import logging

class BabyMonitoringController(module.Base):
    update_rate = 10
    sound_sensor = use_module('SoundSensor')
    alarm_actuator = use_module('AlarmActuator')

    class controller(fields.Base):

        def __init__(self):
            self.decibel_value = 97 #seuil du cri d'un nourisson
            super(BabyMonitoringController.controller, self).__init__()
    
        def always(self):
            print "testons"
            try:
                sound_now = self.module.sound_sensor.sound()[1]
                print 'sound_now= %s' % sound_now
                print 'decibel_limit = %s' % self.decibel_value
            except TypeError as e:
                logger = logging.getLogger()
                logger.exception(e)
            else:
                if sound_now > self.decibel_value:
                    self.module.alarm_actuator.alarm(True)
                    print 'Alert the baby is crying'
                else:
                    self.module.alarm_actuator.alarm(False)
                    print 'Nothing to worry the baby is ok'
    
