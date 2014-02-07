import module
from module import use_module
import fields
import fields.io
import fields.persistant

class TemperatureController(module.Base):
    Temperature = use_module('Temperature')
    TemperatureForecast = use_module('TemperatureForecast')

    temperature_controller = fields.proxy.mix('TemperatureController',
            'Temperature', 'Temperature', 'TemperatureForecast', 'Temperature')

    def always(self):
        """
        if temperature < threshold (desired temperature):
            if temperatureForecast.temperature(t + 1) < threshold:
                # RaiseTheTemperature
            else:
                # LowerTheTemperature
        """
