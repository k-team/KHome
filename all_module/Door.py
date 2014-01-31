from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

if __name__ == '__main__':
    class DoorSensor(core.module.Base):
        update_rate = 10
        class Door(
            core.fields.sensor.Door
            core.fields.io.Readable,
            core.fields.Base):
        pass

    class DoorActuator(core.module.Base):
        class Door(
            core.fields.actuator.Door
            core.fields.io.Writable,
            core.fields.Base):
        pass

    class DoorAccess(core.module.Base):
        update_rate = 10
        doorSensor = use_module('DoorSensor')
        doorActuator = use_module('DoorActuator')

        Door = fields.proxy.mix('Door','DoorSensor', 'Door', 'DoorActuator', 'Door')

