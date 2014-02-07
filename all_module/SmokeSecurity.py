from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time
import all_modules.SmokeSensor
import all_modules.AlarmActuator

class SmokeSecurityController(core.module.Base):
    update_rate = 10
    SMOKE_VALUE = 100
    smoke_sensor = use_module('SmokeSensor')
    alarm_actuator = use_module('AlarmActuator')
    
    class Controller(
        core.fields.Base):
        
        def always(self):
            if smoke_sensor.Smoke() > SMOKE_VALUE:
                alarm_actuator.Alarm(true)
            else
                alarm_actuator.Alarm(false)
