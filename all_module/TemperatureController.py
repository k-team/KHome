from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class TemperatureController(core.module.Base):
    update_rate = 10
    SEUIL = 20
    DELTA_PLUS = 5
    DELTA_MOINS = 7
    temperature = use_module('Temperature')
    temperature_forecast = use_module('TemperatureForecast')
    class Controller(core.fields.Base):
        def always(self):
            if temperature.Temperature < SEUIL
                if temperature_forecast.Temperature > SEUIL + DELTA_PLUS
                    temperature.Temperature = SEUIL
            if temperature.Temperature > SEUIL
                if temperature_forecast.Temperature < SEUIL - DELTA_MOINS
                    temperature.Temperature = SEUIL
