import module
import fields.proxy

class WindowRainManagement(module.Base):
    update_rate = 10
    
    rain = fields.proxy.readable('rain', 'RainForecast', 'rain')
    window_actuator = fields.proxy.writable('window_actuator', 'windowAccess', 'window')

    #management = fields.proxy.mix('management', 'RainForecast', 'rain',
    #       'WindowAccess', 'window')
