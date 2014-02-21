# -*- coding: utf-8 -*-

import module
import fields
import fields.io
import fields.sensor
import fields.persistant
import fields.syntax
import logging

class Interruptor(module.Base):
    update_rate = 1

    class _state(
            fields.io.Hidden,
            fields.sensor.Interruptor,
            fields.io.Readable,
            fields.syntax.Integer,
            fields.persistant.Database,
            fields.Base):
        pass

    class state_a(fields.io.Readable,
            fields.syntax.Numeric,
            fields.persistant.Volatile,
            fields.Base):
        sleep_on_start = 1
        update_rate = 0.1

        def acquire_value(self):
            try:
                v = int(self.module._state()[1]) & 0b0011
            except TypeError as e:
                logging.exception(e)
                return
            if v == 1:
                return -1
            if v == 2:
                return 1
            return 0

    class state_b(fields.io.Readable,
            fields.syntax.Numeric,
            fields.persistant.Volatile,
            fields.Base):
        sleep_on_start = 1
        update_rate = 0.1

        def acquire_value(self):
            try:
                v = int(self.module._state()[1]) & 0b1100
            except TypeError:
                logging.exception(e)
                return
            if v == 4:
                return -1
            if v == 8:
                return 1
            return 0
