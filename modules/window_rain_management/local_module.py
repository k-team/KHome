import module
import fields.proxy

class WindowRainManagement(module.Base):
    update_rate = 10

    management = fields.proxy.mix('Management', 'RainForecast', 'rain',
            'WindowAccess', 'window')
