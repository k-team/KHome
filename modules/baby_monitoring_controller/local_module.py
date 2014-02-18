import module
from module import use_module
import fields
import logging
import fields.syntax

class BabyMonitoringController(module.Base):
    update_rate = 10
    sound_sensor = use_module('SoundSensor')
    alarm_actuator = use_module('AlarmActuator')
    public_name = 'Surveillance du bebe'

    class decibel_value(
            fields.syntax.Constant,
            fields.syntax.Numeric,
            fields.Base):
        const_value = 97.0
        public_name = 'Seuil de detection du crie du bebe'

    class controller(fields.Base):

        def __init__(self):
            super(BabyMonitoringController.controller, self).__init__()

        def always(self):
	    decibel_value = self.module.decibel_value()[1] #seuil du cri d'un nourisson
            print 'testons'
            try:
                sound_now = self.module.sound_sensor.sound()[1]
                print 'sound_now= %s' % sound_now
                print 'decibel_limit = %s' % decibel_value
            except TypeError as e:
                logger = logging.getLogger()
                logger.exception(e)
            else:
                if sound_now > decibel_value:
                    self.module.alarm_actuator.alarm(True)
                    print 'Alert the baby is crying'
                else:
                    self.module.alarm_actuator.alarm(False)
                    print 'Nothing to worry the baby is ok'
    
