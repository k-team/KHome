import module
from module import use_module
import fields

class SmokeSecurityController(module.Base):
    update_rate = 10
    smoke_sensor = use_module('SmokeSensor')
    alarm_actuator = use_module('AlarmActuator')
    
    class controller(fields.Base):
        
        def _init_:
            smoke_value = 20
            super(SmokeSecurityController.controller, self)._init_

        def always(self):
            if self.module.smoke_sensor.smoke() > self.module.smoke_value:
                self.module.alarm_actuator.alarm(True)
            else:
                self.module.alarm_actuator.alarm(False)
