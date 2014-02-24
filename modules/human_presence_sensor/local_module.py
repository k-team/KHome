# -*- coding: utf-8 -*-

import module
import fields

class HumanPresenceSensor(module.Base):
    update_rate = 2
    public_name = 'Capteur de présence'

    class presence(fields.syntax.Boolean, fields.sensor.Presence,
            fields.io.Readable, fields.persistant.Volatile, fields.Base):
        pass
