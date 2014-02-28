# -*- coding: utf-8 -*-

import module
import fields

class FanActuator(module.Base):
    update_rate = 10
    public_name = 'Ventilateur'

    class fan(fields.actuator.Fan, fields.syntax.Boolean, fields.io.Readable,
            fields.persistant.Volatile, fields.Base):
        public_name = 'État du ventilateur'

    class speed(fields.syntax.BoundNumeric,
            fields.io.Readable,
            fields.io.Writable,
            fields.persistant.Volatile,
            fields.Base):
        lower_bound = 1
        upper_bound = 3
        public_name = 'Vitesse du ventilateur'
        init_value = 1
