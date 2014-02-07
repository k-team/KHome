from twisted.internet import reactor
import module
import fields
import fields.io
import fields.persistant
import time

class DoorAccess(module.Base):
    update_rate = 10
    doorSensor = use_module('DoorSensor')
    doorActuator = use_module('DoorActuator')

    Door = fields.proxy.mix('Door',
                            'DoorSensor', 'Door',
                            'DoorActuator', 'Door')
