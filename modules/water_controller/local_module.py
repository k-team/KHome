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
                if self.module.human_presence_sensor.presence(t=-5)[1] && self.module.human_presence_sensor.presence()[1] :
                    if self.module.water_valve_sensor() == False:
                        self.module.water_valve_sensor(True)
                    else:
                        self.module.water_valve_sensor(False)

    class water_valve_sensor(
            fields.sensor.WaterValve,
            fields.actuator.WaterValve,
            fields.persistant.Database,
            fields.Base):
        public_name: 'Bouton switch'
        

    class water_valse_sensor_str(
            fields.syntax.String,
            fields.io.Readable,
            fields.persistant.Volatile,
            fields.Base):
        public_name = 'Etat du robinet'

        def acquire_value(self):
            try:
                return 'Le robinet est ouvert (ON)' if self.module.water_valse_sensor_str()[1] else 'Le robinet est fermé (OFF)'
            except TypeError:
                return

