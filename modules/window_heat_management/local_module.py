import module
import fields.proxy

class WindowHeatManagement(module.Base):
    update_rate = 10
    temperature = fields.proxy.readable('temperature', 'TemperatureForecast', 'temperature')
    window_actuator = fields.proxy.writable('window_actuator', 'WindowAccess', 'window')

   # management = fields.proxy.mix('management', 'TemperatureForecast',
    #        'temperature', 'WindowAccess', 'window')
