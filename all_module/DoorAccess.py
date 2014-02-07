import module
from module import use_module
import fields.proxy

class DoorAccess(module.Base):
    update_rate = 10

    DoorSensor = use_module('DoorSensor')
    DoorActuator = use_module('DoorActuator')

    door = fields.proxy.mix('Door', 'DoorSensor', 'DoorActuator')
