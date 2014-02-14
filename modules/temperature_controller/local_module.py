import module
import fields
from module import use_module

class TemperatureController(module.Base):
    update_rate = 10
    temperature = use_module('Temperature')
    temperature_forecast = use_module('TemperatureForecast')
    class controller(fields.Base):
        def __init__(self):
            self.limit = 20
            self.delta_plus = 5
            self.delta_moins = 7
            self.current_temp = self.module.temperature.temperature()
            self.current_forecast = self.module.temperature_forecast.temperature()
            super(TemperatureController.controller, self).__init__()

        def always(self):
            if self.module.current_temp < self.module.limit:
                if self.module.current_forecast > self.module.limit + self.module.delta_plus:
                    self.module.temperature.temperature(self.module.limit)
                elif self.module.current_forecast < self.module.limit:
                    self.module.temperature.temperature(self.module.limit)
            elif self.module.current_temp > self.module.limit:
                if self.module.current_forecast < self.module.limit - self.module.delta_moins:
                    self.module.temperature.temperature(self.module.limit)
                elif self.module.current_forecast > self.module.limit:
                    self.module.temperature.temperature(self.module.limit)
