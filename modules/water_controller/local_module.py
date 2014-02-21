import module
from module import use_module
import fields
import fields.io
import fields.sensor
import fields.actuator
import fields.persistant

class WaterController(module.Base):
    update_rate = 10

    human_presence_sensor = use_module('HumanPresenceSensor')

    class keep_water_on_duration(fields.syntax.BoundNumeric, fields.io.Writable,
            fields.io.Readable, fields.persistant.Volatile, fields.Base):
        public_name = "Attente (s)"
        lower_bound = 0
        upper_bound = 10

        def on_start(self):
            super(WaterController.keep_water_on_duration, self).on_start()
            self.emit_value((type(self).upper_bound-type(self).lower_bound)/2.0)

    class controller(fields.io.Hidden, fields.Base):
        def always(self):
            limit = self.module.keep_water_on_duration()
            if limit is None:
                return
            limit = limit[1]
            presence = self.module.human_presence_sensor.presence(fr=limit, to=0)
            if any(map(lambda x: x[1], presence)) and self.module.water_valve_sensor()[1]:
                self.module.water_valve_sensor(False)

    class water_valve_sensor(fields.sensor.WaterValve,
            fields.actuator.WaterValve, fields.persistant.Database,
            fields.Base):
        public_name = 'Etat du robinet'
