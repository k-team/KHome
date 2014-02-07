from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class TemperatureController(core.module.Base):
    update_rate = 10
    temperature = use_module('Temperature')
    temperature_forecast = use_module('TemperatureForecast')
    class Controller(core.fields.Base):
        def _init_:
            seuil = 20
            delta_plus = 5
            delta_moins = 7
            super(TemperatureController, self)._init_
        def always(self):
            if temperature.Temperature() < seuil
                if temperature_forecast.Temperature() > seuil + delta_plus
                    temperature.Temperature(seuil)
                if temperature_forecast.Temeprature() < seuil
                    temperature.Temperature(seuil)
            if temperature.Temperature() > seuil
                if temperature_forecast.Temperature() < seuil - delta_moins
                    temperature.Temperature(seuil)
                if temperature_forecast.Temeprature() > seuil
                    temperature.Temperature(seuil)
