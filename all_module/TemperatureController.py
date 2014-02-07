from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time
import all_modules.temperature

if __name__ == '__main__':
    class TemperatureController(core.module.Base)
        temperature = use_module('Temperature')
        temperatureForecast = use_module('TemperatureForecast')

        TemperatureController = fields.proxy.mix('TemperatureController',
                                   		 'Temperature', 'Temperature',
                                   		 'TemperatureForecast', 'Temperature')
        def always(self):
            '''
            if temperature < threshold (desired temperature)
							if temperatureForecast.temperature(t + 1) < threshold
								RaiseTheTemperature
							else 
								LowerTheTemperature
						'''
