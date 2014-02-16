import module
import fields.proxy

class WindowRainManagement(module.Base):
    update_rate = 10
    
    management = fields.proxy.mix('management', 'RainForecast', 'rain',
            'WindowAccess', 'window')
