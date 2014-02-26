# -*- coding: utf-8 -*-

import module
import fields
from module import use_module

class Door(module.Base):
    public_name = 'Porte automatique'
    update_rate = 10

    twitter = use_module('twitter')

    class state(fields.sensor.Contact, fields.actuator.Door,
            fields.persistant.Database, fields.Base):
        public_name = 'État de la porte'

        def set_value(self, time, value):
            if value:
                self.module.twitter.tweet('La porte est correctement fermée.')
            else:
                self.module.twitter.tweet('La porte est ouverte #cambriolage')

            return super(Door.state, self).set_value(time, value)
