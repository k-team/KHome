import module
import fields
import fields.sensor
import fields.actuator
import fields.io
import fields.persistant
from module import use_module

class WaterController(module.Base):
    update_rate = 10
    human_presence_sensor = use_module('HumanPresenceSensor')
    class controller(fields.Base):

        def __init__(self):
            super(WaterController.controller, self).__init__()

        def always(self):
            if self.module.human_presence_sensor.presence() and self.module.water_valve_sensor() == 'FERME':
                self.module.water_valve_actuator('OPEN')
            elif not self.module.human_presence_sensor.presence() and self.module.water_valve_sensor() == 'OPEN':
                self.module.water_valve_actuator('CLOSE')

    class water_valve_sensor(
            fields.sensor.WaterValve,
            fields.io.Readable,
            fields.persistant.Volatile,
            fields.Base):
        pass

    class water_valve_actuator(
            fields.actuator.WaterValve,
            fields.io.Writable,
            fields.Base):
                pass
