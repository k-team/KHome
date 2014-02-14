import module
from module import use_module
import fields.proxy

class DoorAccess(module.Base):
    update_rate = 10

    doorSensor = use_module('DoorSensor')
    doorActuator = use_module('DoorActuator')

    door = fields.proxy.mix('Door', 'DoorSensor', 'DoorActuator')
