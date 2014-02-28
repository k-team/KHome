#-*- coding: utf-8 -*-
import module
import fields

class PowerPlug(module.Base):
    public_name = 'Prise électrique'

    class plug(fields.actuator.PowerPlug, fields.syntax.Boolean,
            fields.persistant.Volatile, fields.Base):
        public_name = 'Prise'
