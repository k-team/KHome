import module
import fields
from module import use_module

class WaterController(module.Base):
    update_rate = 10
    water_valve_sensor = use_module('WaterValve')
    water_valve_actuator = use_module('WaterValveActuator')
    human_presence_sensor = use_module('HumanPresenceSensor')
    class controller(fields.Base):

        def _init_:
            super(WaterController.controller, self)._init_

        def always(self):
            if self.module.human_presence_sensor.presence():
                and self.module.water_valve_sensor.waterValve() == 'FERME':
                    self.module.water_valve_actuator.waterValve('OPEN')
            elif not self.module.human_presence_sensor.presence()
                and self.module.water_valve_sensor.water_valve() == 'OPEN':
                    self.module.water_valve_actuator.water_valve('CLOSE')
