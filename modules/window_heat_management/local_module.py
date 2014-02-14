import module
import fields.proxy

class WindowHeatManagement(module.Base):
    update_rate = 10

    management = fields.proxy.mix('Management', 'TemperatureForecast',
            'temperature', 'WindowAccess', 'window')
