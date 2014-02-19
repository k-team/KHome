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
    update_rate = 30 * 60
    public_name = 'Météo'

    class _weather(
            fields.io.Hidden,
            fields.io.Readable,
            fields.persistant.Volatile,
            fields.Base):
        sleep_on_start = 0.5

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
                        'country': ans.location.country,
                        'wind_speed': ans.wind.speed,
                        'wind_direction': ans.wind.cardinal_direction()
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
            self.emit_value(609125) # Lyon

        # def acquire_value(self):
        #     woeid = 609125 # Lyon
        #     return woeid

    class temperature(
            fields.syntax.Numeric,
            fields.io.Graphable,
            fields.persistant.Volatile,
            fields.Base):
        public_name = 'Température (°C)'
        sleep_on_start = 2

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
        sleep_on_start = 2

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
        public_name = 'Pression (mbars)'
        sleep_on_start = 2

        def acquire_value(self):
            try:
                return self.module._weather()[1]['pressure']
            except TypeError:
                return

    class wind_speed(
            fields.syntax.Numeric,
            fields.io.Graphable,
            fields.persistant.Volatile,
            fields.Base):
        public_name = 'Vitesse du vent (km/h)'
        sleep_on_start = 2

        def acquire_value(self):
            try:
                return self.module._weather()[1]['wind_speed']
            except TypeError:
                return

    class wind_direction(
            fields.syntax.String,
            fields.io.Readable,
            fields.persistant.Volatile,
            fields.Base):
        public_name = 'Direction du vent'
        sleep_on_start = 2

        def acquire_value(self):
            try:
                direction = {None: 'Pas de vent', 
                        'N': 'Nord',
                        'S': 'Sud',
                        'E': 'Est',
                        'W': 'Ouest'}
                return direction[self.module._weather()[1]['wind_direction']]
            except (KeyError, TypeError):
                return

    class city(
            fields.syntax.String,
            fields.persistant.Volatile,
            fields.io.Readable,
            fields.Base):
        public_name = 'Ville'
        sleep_on_start = 2

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
        sleep_on_start = 2

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
        sleep_on_start = 2

        def acquire_value(self):
            try:
                return self.module._weather()[1]['country']
            except TypeError:
                return
