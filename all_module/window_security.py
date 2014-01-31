from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

if __name__ == '__main__':

    class WindowSecurity(core.module.Base):
        update_rate = 10
        windowAcces = use_module('WindowAccess')
        recognition = use_module('Recognition')
        alarmActuator = use_module('AlarmActuator')

        Security = fields.proxy.mix('Security',
        														'WindowAccess','Window',
        														'Recognition','Recognize', 
        														'AlarmActuator','Alarm')
