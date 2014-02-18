# -*- coding: utf-8 -*-

import module
import weatherpy
import fields
import fields.io
import fields.sensor
import fields.persistant
import fields.syntax

class Weather(module.Base):
    update_rate = 60
    public_name = 'Météo'

    class woeid(fields.persistant.Volatile,
            fields.syntax.Numeric,
            fields.io.Writable,
            fields.io.Readable,
            fields.Base):
        public_name = 'Géolocalisation'

        def acquire_value(self):
            woeid = 609125 # Lyon
            return woeid

    class temperature(
            fields.syntax.Numeric,
            fields.io.Graphable,
            fields.persistant.Volatile,
            fields.Base):
        public_name = 'Température (°C)'

        def acquire_value(self):
            try:
                woeid = self.module.woeid()[1]
                ans = weatherpy.Response('User-KHome', woeid, metric=True)
                return ans.condition.temperature
            except (IOError, TypeError):
                return

    class humidity(
            fields.syntax.Numeric,
            fields.io.Graphable,
            fields.persistant.Volatile,
            fields.Base):
        public_name = 'Humidité (%)'

        def acquire_value(self):
            try:
                woeid = self.module.woeid()[1]
                ans = weatherpy.Response('User-KHome', woeid, metric=True)
                return ans.atmosphere.humidity
            except (IOError, TypeError):
                return

    class pressure(
            fields.syntax.Numeric,
            fields.io.Graphable,
            fields.persistant.Volatile,
            fields.Base):
        public_name = 'Pression (Pa)'

        def acquire_value(self):
            try:
                woeid = self.module.woeid()[1]
                ans = weatherpy.Response('User-KHome', woeid, metric=True)
                return ans.atmosphere.pressure
            except (IOError, TypeError):
                return

    class city(
            fields.syntax.String,
            fields.persistant.Volatile,
            fields.io.Readable,
            fields.Base):
        public_name = 'Ville'

        def acquire_value(self):
            try:
                woeid = self.module.woeid()[1]
                ans = weatherpy.Response('User-KHome', woeid, metric=True)
                return ans.location.city
            except (IOError, TypeError):
                return

    class region(
            fields.syntax.String,
            fields.persistant.Volatile,
            fields.io.Readable,
            fields.Base):
        public_name = 'Région'

        def acquire_value(self):
            try:
                woeid = self.module.woeid()[1]
                ans = weatherpy.Response('User-KHome', woeid, metric=True)
                return ans.location.region
            except (IOError, TypeError):
                return

    class country(
            fields.syntax.String,
            fields.persistant.Volatile,
            fields.io.Readable,
            fields.Base):
        public_name = 'Pays'

        def acquire_value(self):
            try:
                woeid = self.module.woeid()[1]
                ans = weatherpy.Response('User-KHome', woeid, metric=True)
                return ans.location.country
            except (IOError, TypeError):
                return
