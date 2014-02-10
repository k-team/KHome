import module
import fields
import fields.io
import fields.persistant
import fields.proxy
import fields.sensor
import fields.actuator
from module import use_module

class WaterController(core.module.Base):
    update_rate = 10
    water_valve_sensor = use_module('WaterValve')
    water_valve_actuator = use_module('WaterValveActuator')
    human_presence_sensor = use_module('HumanPresenceSensor')
    class controller(core.fields.Base):
        def always(self):
            if human_presence_sensor.Presence():
                and water_valve_sensor.WaterValve() == 'FERME':
                    water_valve_actuator.WaterValve('OPEN')
            elif not human_presence_sensor.Presence()
                and water_valve_sensor.WaterValve() == 'OPEN':
                    water_valve_actuator.WaterValve('CLOSE')
