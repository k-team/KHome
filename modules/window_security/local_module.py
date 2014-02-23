import module
from module import use_module
import fields
import logging

class WindowSecurity(module.Base):
    update_rate = 10
    window_access = use_module('Window')
    recognition = use_module('Recognition')
    alarm = use_module('Alarm')

    class controller(fields.Base):
        def __init__(self):
            super(WindowSecurity.controller, self).__init__()

        def always(self):
            print 'testons'
            try:
                window_status = self.module.window_access.state()
                recognition_status = self.module.recognition.recognised()
                print 'window_status = %s, recognition_status = %s' % (window_status, recognition_status)
            except TypeError as e:
                logger = logging.getLogger()
                logger.exception(e)
            else:
                if window_status == 'OPEN' and recognition_status == 'UNKNOWN':
                    self.module.alarm.message('Alert Unknown person in the house')
                    print

