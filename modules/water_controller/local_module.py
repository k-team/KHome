# -*- coding: utf-8 -*-

import module
from module import use_module
import fields

class WaterController(module.Base):
    update_rate = 10

    human_presence_sensor = use_module('HumanPresenceSensor')

    class keep_water_on_duration(fields.syntax.BoundNumeric, fields.io.Writable,
            fields.io.Readable, fields.persistant.Volatile, fields.Base):
        public_name = "Attente (s)"
        lower_bound = 0
        upper_bound = 10
        init_value = abs(upper_bound - lower_bound) / 2.

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
            fields.actuator.WaterValve, fields.persistant.Volatile,
            fields.Base):
        public_name = 'État du robinet'
