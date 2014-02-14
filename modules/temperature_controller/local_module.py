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
            self.current_temp = temperature.temperature()
            self.current_forecast = temperature_forecast.temperature()
            super(TemperatureController.controller, self).__init__()

        def always(self):
            if self.current_temp < self.limit:
                if self.current_forecast > self.limit + self.delta_plus:
                    self.temperature.temperature(self.limit)
                elif self.current_forecast < self.limit:
                    self.temperature.temperature(self.limit)
            elif self.current_temp > self.limit:
                if self.current_forecast < self.limit - self.delta_moins:
                    self.temperature.temperature(self.limit)
                elif self.current_forecast > self.limit:
                    self.temperature.temperature(self.limit)
