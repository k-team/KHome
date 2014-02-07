import module
import fields.proxy

class DoorRainManagement(module.Base):
    update_rate = 10
    management = fields.proxy.mix('Management', 'RainForecast', 'Rain',
            'DoorAccess', 'Door')
