import module
from module import use_module
import fields
import logging

class WindowSecurity(module.Base):
    update_rate = 10
    windowAccess = use_module('WindowAccess')
    recognition = use_module('Recognition')
    alarmActuator = use_module('AlarmActuator')

    class controller(fields.Base):
        def __init__(self):
            super(WindowSecurity.controller, self).__init__()

        def always(self):
            print 'testons'
            try:
                window_status = self.module.window_access.window()
                recognition_status = self.module.recognition.recognised()
                print 'window_status = %s, recognition_status = %s' % (window_status, recognition_status)
            except TypeError as e:
                logger = logging.getLogger()
                logger.exception(e)
            else:
                if window_status == 'OPEN' and recognition_status == 'UNKNOWN':
                    self.module.alarm_actuator.alarm(True)
                    print 'Alert Unknown person in the house'
                else:
                    self.module.alarm_actuator.alarm(False)
                    print 'Nothing to worry the house is safe'

