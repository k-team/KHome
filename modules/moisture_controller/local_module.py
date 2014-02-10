from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time
import all_modules.MoistureSensor
import all_modules.FanActuator

class MoistureController(core.module.Base):
    update_rate = 10
    moisture_sensor = use_module('MoistureSensor')
    fan_actuator = use_module('FanActuator')
    class Controller(core.fields.Base):
        
        def _init_:
            MOISTURE_VALUE = 100
            super(Controller, self)._init_

        def always(self):
            if moisture_sensor.Moisture > MOISTURE_VALUE
                fan_actuator.Fan(true)
            else
                fan_actuator.Fan(false)
