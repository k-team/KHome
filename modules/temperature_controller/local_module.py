import module
from module import use_module
import fields

class TemperatureController(module.Base):
    update_rate = 10
    temperature = use_module('Temperature')
    temperature_forecast = use_module('TemperatureForecast')

    class limit(fields.io.Readable, fields.syntax.Numeric,
            fields.persistant.Volatile, fields.Base):
        def on_start(self):
            self.emit_value(20)
            super(TemperatureController.limit).on_start()

    class controller(fields.Base):
        def __init__(self):
            super(TemperatureController.controller, self).__init__()

            # TODO configure these ?
            self.delta_up = 5
            self.delta_down = 7

        def always(self):
            try:
                current_temp = self.module.temperature.temperature()[1]
                current_forecast = self.module.temperature_forecast.temperature()[1]
                limit = self.module.limit()[1]
            except TypeError:
                pass # ignore
            else:
                if current_temp < limit:
                    if current_forecast > limit + self.delta_up:
                        self.module.temperature.temperature(limit)
                    elif current_forecast < self.module.limit:
                        self.module.temperature.temperature(limit)
                elif current_temp > limit:
                    if current_forecast < limit - self.delta_down:
                        self.module.temperature.temperature(limit)
                    elif current_forecast > limit:
                        self.module.temperature.temperature(limit)
