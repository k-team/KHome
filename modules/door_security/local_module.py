import module
from module import use_module
import fields
import logging

class DoorSecurity(module.Base):
    update_rate = 10
    door_access = use_module('DoorAccess')
    recognition = use_module('Recognition')
    alarm_actuator = use_module('AlarmActuator')

    class controller(fields.Base):
        def __init__(self):
            super(DoorSecurity.controller, self).__init__()

        def always(self):
            print 'testons'
            try:
                door_status = self.module.door_access.door()
                recognition_status = self.module.recognition.recognised()
                print 'door_status = %s, recognition_status = %s' % (door_status, recognition_status)
            except TypeError as e:
                logger = logging.getLogger()
                logger.exception(e)
            else:
                if door_status == 'OPEN' and recognition_status == 'UNKNOWN':
                    self.module.alarm_actuator.alarm(True)
                    print 'Alert Unknown person in the house'
                else:
                    self.module.alarm_actuator.alarm(False)
                    print 'Nothing to worry the house is safe'
