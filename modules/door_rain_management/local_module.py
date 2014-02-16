import module
import fields.proxy

class DoorRainManagement(module.Base):
    update_rate = 10

    rain = fields.proxy.readable('rain', 'RainForecast', 'rain')
    door_actuator = fields.proxy.writable('door_actuator', 'DoorAccess', 'door')

    #management = fields.proxy.mix('management', 'RainForecast', 'rain',
    #       'DoorAccess', 'door')
