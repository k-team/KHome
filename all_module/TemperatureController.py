import module
from module import use_module
import fields
import fields.io
import fields.persistant

# module constants
LIMIT = 20
UP_DELTA = 5
DOWN_DELTA = 7

# dependencies
temperature = use_module('Temperature')
temperature_forecast = use_module('TemperatureForecast')

class TemperatureController(module.Base):
    update_rate = 10

    class Controller(fields.Base):
        def always(self):
            if temperature.temperature < LIMIT:
                if temperature_forecast.temperature > LIMIT + UP_DELTA:
                    temperature.temperature = LIMIT
            if temperature.temperature > LIMIT:
                if temperature_forecast.temperature < LIMIT - DOWN_DELTA:
                    temperature.Temperature = LIMIT
