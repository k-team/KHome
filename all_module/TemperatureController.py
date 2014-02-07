import module
from module import use_module
import fields

# module constants
LIMIT = 20
UP_DELTA = 5
DOWN_DELTA = 7

class TemperatureController(module.Base):
    update_rate = 10

    temperature = use_module('Temperature')
    temperature_forecast = use_module('TemperatureForecast')

    class controller(fields.Base):
        def __init__(self):
            self.limit = 20
            self.delta_plus = 5
            self.delta_moins = 7
            super(TemperatureController.controller, self).__init__()

        def always(self):
            temperature = self.module.temperature
            measured_temperature = temperature.temperature()
            temperature_forecast = self.module.temperature_forecast.temperature()
            if measured_temperature < self.limit:
                if temperature_forecast > self.limit + self.delta_plus:
                    temperature.temperature(self.limit)
                if temperature_forecast < self.limit:
                    temperature.temperature(self.limit)
            if measured_temperature > self.limit:
                if temperature_forecast < self.limit - self.delta_moins:
                    temperature.temperature(self.limit)
                if temperature_forecast > self.limit:
                    temperature.temperature(self.limit)
