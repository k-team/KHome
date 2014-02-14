import module
from module import use_module
import fields

class MoistureController(module.Base):
    update_rate = 10
    moisture_sensor = use_module('MoistureSensor')
    fan_actuator = use_module('FanActuator')
    class controller(fields.Base):

        def __init__(self):
            self.moisture_value = 45 #faut le considérer en pourcentage
            super(MoistureController.controller, self).__init__()

        def always(self):
            if self.module.moisture_sensor.moisture() > self.moisture_value:
                self.module.fan_actuator.fan(True)
            else:
                self.module.fan_actuator.fan(False)
