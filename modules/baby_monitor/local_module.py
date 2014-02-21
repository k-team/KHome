#-*- coding: utf8 -*-

import module
from module import use_module
import fields
import fields.io
import fields.persistant
import fields.syntax
import logging

class BabyMonitor(module.Base):
    update_rate = 4.2
    sound_sensor = use_module('SoundSensor')
    alarm = use_module('Alarm')
    public_name = 'Babyphone'

    class decibel_value(
            fields.syntax.Numeric,
            fields.io.Readable,
            fields.persistant.Database,
            fields.Base):
        public_name = 'Seuil de detection du bébé'
        update_rate = 421337

        def on_start(self):
            super(BabyMonitor.decibel_value, self).on_start()
            self.emit_value(97.0)

    class controller(fields.io.Hidden,
            fields.Base):
        sleep_on_start = 1

        def always(self):
            try:
                decibel_value = self.module.decibel_value()[1]
                sound_now = self.module.sound_sensor.sound()[1]
            except TypeError as e:
                logging.exception(e)
            else:
                if sound_now > decibel_value:
                    self.module.alarm.alarm(True)
                    self.module.alarm.message('Le bébé est en train de pleurer.')
