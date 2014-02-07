import module
import fields.proxy

class DoorHeatManagement(module.Base):
    update_rate = 10

    management = fields.proxy.mix('Management', 'TemperatureForecast',
            'Temperature', 'DoorAccess', 'Door')
