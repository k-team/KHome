import module
import fields
from module import use_module

class WaterController(module.Base):
    update_rate = 10
    water_valve_sensor = use_module('WaterValveSensor')
    water_valve_actuator = use_module('WaterValveActuator')
    human_presence_sensor = use_module('HumanPresenceSensor')
    class controller(fields.Base):

        def __init__(self):
            super(WaterController.controller, self).__init__()

        def always(self):
            if self.module.human_presence_sensor.presence() and self.module.water_valve_sensor.water_valve() == 'FERME':
                self.module.water_valve_actuator.water_valve('OPEN')
            elif not self.module.human_presence_sensor.presence() and self.module.water_valve_sensor.water_valve() == 'OPEN':
                self.module.water_valve_actuator.water_valve('CLOSE')
