import module
import fields
import fields.io
import fields.persistant
import fields.syntax
from module import use_module

class TemperatureController(module.Base):
    update_rate = 10
    temperature = use_module('Temperature')
    temperature_forecast = use_module('TemperatureForecast')

    class limit(fields.io.Readable,
        fields.syntax.Numeric,
        fields.persistant.Volatile,
        fields.Base):
        def __init__(self):
            super(TemperatureController.limit, self).__init__()
            self.emit_value(20)
        
    class controller(fields.Base):
        def __init__(self):
            super(TemperatureController.controller, self).__init__()
            self.delta_plus = 5
            self.delta_moins = 7

        def always(self):
            try:
                current_temp = self.module.temperature.temperature()[1]
                current_forecast = self.module.temperature_forecast.temperature()[1]
                limit = self.module.limit()[1]
            except TypeError:
                pass # Ignore
            else:
                if current_temp < limit:
                    if current_forecast > limit + self.delta_plus:
                        self.module.temperature.temperature(limit)
                    elif current_forecast < self.module.limit:
                        self.module.temperature.temperature(limit)
                elif current_temp > limit:
                    if current_forecast < limit - self.delta_moins:
                        self.module.temperature.temperature(limit)
                    elif current_forecast > limit:
                        self.module.temperature.temperature(limit)
