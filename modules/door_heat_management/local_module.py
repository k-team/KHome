import module
import fields.proxy

class DoorHeatManagement(module.Base):
    update_rate = 10
    temperature = fields.proxy.readable('temperature', 'TemperatureForecast', 'temperature')
    door_actuator = fields.proxy.writable('door_actuator', 'DoorAccess', 'door')

#    management = fields.proxy.mix('management', 'TemperatureForecast',
#            'temperature', 'DoorAccess', 'door')
