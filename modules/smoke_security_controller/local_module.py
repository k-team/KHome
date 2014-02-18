import module
from module import use_module
import fields
import logging

class SmokeSecurityController(module.Base):
    update_rate = 10
    smoke_sensor = use_module('SmokeSensor')
    alarm_actuator = use_module('AlarmActuator')
    
    class controller(fields.Base):
        
        def __init__(self):
            self.smoke_value_limit = 20
            super(SmokeSecurityController.controller, self).__init__()

        def always(self):
            print 'testons'
            try:
                smoke_value = self.module.smoke_sensor.smoke()[1]
                print 'smoke_value = %s, smoke_value_limit = %s' % (smoke_value, self.smoke_value_limit)
            except TypeError as e:
                logger = logging.getLogger()
                logger.exception(e)
            else:
                if smoke_value > self.smoke_value_limit:
                    print 'Alarm There is a lot of smoke in the house'
                    self.module.alarm_actuator.alarm(True)
                else:
                    print 'Nothing to worry no smoke in the house'
                    self.module.alarm_actuator.alarm(False)
