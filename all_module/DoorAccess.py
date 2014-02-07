from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time
import all_modules.DoorSensor
import all_modules.DoorActuator

class DoorAccess(core.module.Base):
    update_rate = 10
    doorSensor = use_module('DoorSensor')
    doorActuator = use_module('DoorActuator')

    Door = fields.proxy.mix('Door',
                            'DoorSensor', 'Door', 
                            'DoorActuator', 'Door')
