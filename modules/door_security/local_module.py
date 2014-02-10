import module
from module import use_module
import fields
import fields.proxy

class DoorSecurity(module.Base):
    update_rate = 10
    door_access = use_module('DoorAccess')
    recognition = use_module('Recognition')
    alarm_actuator = use_module('AlarmActuator')

    class Controller(fields.Base):
        def always(self):
            if self.module.door_access.door() == 'OPEN' and self.module.recognition.recognised() == 'UNKOWN':
                self.module.alarm_actuator.alarm(True)
            else:
                self.module.alarm_actuator.alarm(False)
