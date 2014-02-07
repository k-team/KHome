import module
import fields
import fields.io
import fields.persistant
import fields.proxy
import fields.sensor
import fields.actuator
from module import use_module

class TemperatureController(core.module.Base):
    update_rate = 10
    temperature = use_module('Temperature')
    temperature_forecast = use_module('TemperatureForecast')
    class controller(core.fields.Base):
        def _init_:
            limit = 20
            delta_plus = 5
            delta_moins = 7
            super(TemperatureController, self)._init_
        def always(self):
            current_temp = temperature.Temperature()
            current_forecast = temperature_forecast.Temperature()
            if current_temp < limit:
                if current_forecast > limit + delta_plus:
                    temperature.Temperature(limit)
                elif current_forecast < limit:
                    temperature.Temperature(limit)
            elif current_temp > limit:
                if current_forecast < limit - delta_moins:
                    temperature.Temperature(limit)
                elif current_forecast > limit:
                    temperature.Temperature(limit)
