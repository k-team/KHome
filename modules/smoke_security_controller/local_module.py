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
            if self.module.smoke_sensor.smoke() > self.module.smoke_value:
                self.module.alarm_actuator.alarm(True)
            else:
                self.module.alarm_actuator.alarm(False)
