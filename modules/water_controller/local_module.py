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
    public_name = 'Robinet'

    class controller(fields.io.Hidden, fields.Base):

        def __init__(self):
            super(WaterController.controller, self).__init__()

        def always(self):
                if self.module.human_presence_sensor.presence():
                    if self.module.water_valve_sensor() == False:
                        self.module.water_valve_sensor(True)
                    else:
                        self.module.water_valve_sensor(False)

    class water_valve_sensor(
            fields.sensor.WaterValve,
            fields.actuator.WaterValve,
            fields.persistant.Database,
            fields.Base):
        public_name = 'Etat du robinet'

   # class water_valve_actuator(
    #        fields.io.Writable,
     #       fields.Base):
      #    pass
