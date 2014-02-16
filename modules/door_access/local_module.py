import module
import fields.proxy

class DoorAccess(module.Base):
    update_rate = 10

    door = fields.proxy.mix('door', 'DoorSensor', 'door', 'DoorActuator', 'door')
