# -*- coding: utf-8 -*-

import module
import fields

class Door(module.Base):
    public_name = 'Porte automatique'
    update_rate = 10

    class state(fields.sensor.Contact, fields.actuator.Door,
            fields.persistant.Volatile, fields.Base):
        public_name = 'État de la porte'
