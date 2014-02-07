from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class WaterController(core.module.Base):
    update_rate = 10
    water_valve_sensor = use_module('WaterValve')
    water_valve_actuator = use_module('WaterValveActuator')
    human_presence_sensor = use_module('HumanPresenceSensor')
    class Controller(core.fields.Base):
        if human_presence_sensor.Presence()
            and water_valve_sensor.WaterValve() == 'FERME':
                water_valve_actuator.WaterValve('OPEN')
        if not human_presence_sensor.Presence()
            and water_valve_sensor.WaterValve() == 'OPEN':
                water_valve_actuator.WaterValve('CLOSE')
