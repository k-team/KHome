import module
from module import use_module
import fields

class SmokeSecurityController(module.Base):
    update_rate = 10
    smoke_sensor = use_module('SmokeSensor')
    alarm_actuator = use_module('AlarmActuator')
    
    class controller(fields.Base):
        
        def __init__(self):
            self.smoke_value = 20
            super(SmokeSecurityController.controller, self).__init__()

        def always(self):
	    print "smoke sensor = %s " % self.module.smoke_sensor.smoke()[1]
            if self.module.smoke_sensor.smoke()[1] > self.smoke_value:
	        print "Alarme"
                self.module.alarm_actuator.alarm(True)
            else:
                print "pas alarme"
                self.module.alarm_actuator.alarm(False)
