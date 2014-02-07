from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time
import all_modules.DoorAccess
import all_modules.Recognition
import all_modules.AlarmActuator

class DoorSecurity(core.module.Base):
    update_rate = 10
    door_access = use_module('DoorAccess')
    recognition = use_module('Recognition')
    alarm_actuator = use_module('AlarmActuator')
    
    class Controller(
        core.fields.Base):
        
        def always(self):
            if (door_access.Door() == "OPEN" and 
                recognition.Recognised() == "UNKOWN"):
                alarm_actuator.Alarm(true)
            else
                alarm_actuator.Alarm(false)
