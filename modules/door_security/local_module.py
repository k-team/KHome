import module
from module import use_module
import fields

class DoorSecurity(module.Base):
    update_rate = 10
    door_access = use_module('DoorAccess')
    recognition = use_module('Recognition')
    alarm_actuator = use_module('AlarmActuator')

    class controller(fields.Base):
        
        def _init_:
            super(BabyMonitoringController.controller, self)._init_

        def always(self):
            if self.module.door_access.door() == 'OPEN' and self.module.recognition.recognised() == 'UNKOWN':
                self.module.alarm_actuator.alarm(True)
            else:
                self.module.alarm_actuator.alarm(False)
