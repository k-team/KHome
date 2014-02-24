# -*- coding: utf-8 -*-

import module
import weatherpy
import fields

class Weather(module.Base):
    update_rate = 30 * 60
    public_name = 'Météo'

    class _weather(fields.io.Hidden, fields.io.Readable,
            fields.persistant.Volatile, fields.Base):
        sleep_on_start = 0.5

        def acquire_value(self):
            try:
                woeid = int(self.module.woeid()[1])
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
                self.module.logger.exception(e)

    class woeid(fields.syntax.Integer, fields.io.Writable, fields.io.Readable,
            fields.persistant.Volatile, fields.Base):
        public_name = 'Géolocalisation (WOEID)'

        def on_start(self):
            super(Weather.woeid, self).on_start()
            self.emit_value(609125) # Lyon

        # def acquire_value(self):
        #     woeid = 609125 # Lyon
        #     return woeid

    class temperature(fields.syntax.Numeric, fields.io.Graphable,
            fields.persistant.Database, fields.Base):
        public_name = 'Température (°C)'
        sleep_on_start = 2

        def acquire_value(self):
            try:
                return self.module._weather()[1]['temperature']
            except TypeError:
                pass

    class humidity(fields.syntax.Percentage, fields.io.Graphable,
            fields.persistant.Database, fields.Base):
        public_name = 'Humidité (%)'
        sleep_on_start = 2

        def acquire_value(self):
            try:
                return self.module._weather()[1]['humidity']
            except TypeError:
                pass

    class pressure(fields.syntax.Numeric, fields.io.Graphable,
            fields.persistant.Database, fields.Base):
        public_name = 'Pression (mbars)'
        sleep_on_start = 2

        def acquire_value(self):
            try:
                return self.module._weather()[1]['pressure']
            except TypeError:
                pass

    class wind_speed(fields.syntax.Numeric, fields.io.Graphable,
            fields.persistant.Database, fields.Base):
        public_name = 'Vitesse du vent (km/h)'
        sleep_on_start = 2

        def acquire_value(self):
            try:
                return self.module._weather()[1]['wind_speed']
            except TypeError:
                pass

    class wind_direction(fields.syntax.String, fields.io.Readable,
            fields.persistant.Volatile, fields.Base):
        public_name = 'Direction du vent'
        sleep_on_start = 2

        def acquire_value(self):
            try:
                direction = {
                        None: 'Pas de vent',
                        'N': 'Nord',
                        'S': 'Sud',
                        'E': 'Est',
                        'W': 'Ouest'
                        }
                return direction[self.module._weather()[1]['wind_direction']]
            except (KeyError, TypeError):
                pass

    class city(fields.syntax.String, fields.persistant.Volatile,
            fields.io.Readable, fields.Base):
        public_name = 'Ville'
        sleep_on_start = 2

        def acquire_value(self):
            try:
                return self.module._weather()[1]['city']
            except TypeError:
                pass

    class region(fields.syntax.String, fields.persistant.Volatile,
            fields.io.Readable, fields.Base):
        public_name = 'Région'
        sleep_on_start = 2

        def acquire_value(self):
            try:
                return self.module._weather()[1]['region']
            except TypeError:
                pass

    class country(fields.syntax.String, fields.persistant.Volatile,
            fields.io.Readable, fields.Base):
        public_name = 'Pays'
        sleep_on_start = 2

        def acquire_value(self):
            try:
                return self.module._weather()[1]['country']
            except TypeError:
                pass
