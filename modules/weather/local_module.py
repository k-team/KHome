# -*- coding: utf-8 -*-

import module
import weatherpy
import fields
import fields.io
import fields.sensor
import fields.persistant
import fields.syntax
import logging

class Weather(module.Base):
    update_rate = 2
    public_name = 'Météo'

    class _weather(
            fields.io.Hidden,
            fields.io.Readable,
            fields.persistant.Volatile,
            fields.Base):
        def acquire_value(self):
            try:
                woeid = self.module.woeid()[1]
                ans = weatherpy.Response('User-KHome', woeid, metric=True)
                return {
                        'temperature': ans.condition.temperature,
                        'humidity': ans.atmosphere.humidity,
                        'pressure': ans.atmosphere.pressure,
                        'city': ans.location.city,
                        'region': ans.location.region,
                        'country': ans.location.country
                }
            except (AssertionError, IOError, TypeError) as e:
                logging.exception(e)
                return

    class woeid(
            fields.syntax.Integer,
            fields.io.Writable,
            fields.io.Readable,
            fields.persistant.Volatile,
            fields.Base):
        public_name = 'Géolocalisation'

        def on_start(self):
            super(Weather.woeid, self).on_start()
            print self.get_info()
            self.emit_value(609125)

        # def acquire_value(self):
        #     woeid = 609125 # Lyon
        #     return woeid

    class temperature(
            fields.syntax.Numeric,
            fields.io.Graphable,
            fields.persistant.Volatile,
            fields.Base):
        public_name = 'Température (°C)'

        def acquire_value(self):
            try:
                return self.module._weather()[1]['temperature']
            except TypeError:
                return

    class humidity(
            fields.syntax.Numeric,
            fields.io.Graphable,
            fields.persistant.Volatile,
            fields.Base):
        public_name = 'Humidité (%)'

        def acquire_value(self):
            try:
                return self.module._weather()[1]['humidity']
            except TypeError:
                return

    class pressure(
            fields.syntax.Numeric,
            fields.io.Graphable,
            fields.persistant.Volatile,
            fields.Base):
        public_name = 'Pression (Pa)'

        def acquire_value(self):
            try:
                return self.module._weather()[1]['pressure']
            except TypeError:
                return

    class city(
            fields.syntax.String,
            fields.persistant.Volatile,
            fields.io.Readable,
            fields.Base):
        public_name = 'Ville'

        def acquire_value(self):
            try:
                return self.module._weather()[1]['city']
            except TypeError:
                return

    class region(
            fields.syntax.String,
            fields.persistant.Volatile,
            fields.io.Readable,
            fields.Base):
        public_name = 'Région'

        def acquire_value(self):
            try:
                return self.module._weather()[1]['region']
            except TypeError:
                return

    class country(
            fields.syntax.String,
            fields.persistant.Volatile,
            fields.io.Readable,
            fields.Base):
        public_name = 'Pays'

        def acquire_value(self):
            try:
                return self.module._weather()[1]['country']
            except TypeError:
                return
