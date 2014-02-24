# -*- coding: utf-8 -*-

import module
import fields

class MethaneGaz(module.Base):
    public_name = 'Gestionnaire de méthane'

    class methane(fields.sensor.Methane, fields.syntax.Numeric,
            fields.io.Graphable, fields.persistant.Database, fields.Base):
        public_name = 'Taux de méthane'

    class gaz_actuator(fields.actuator.Methane, fields.syntax.Boolean,
            fields.io.Readable, fields.persistant.Volatile, fields.Base):
        public_name = 'Robinet de méthane'
