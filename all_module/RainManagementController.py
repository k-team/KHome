from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class RainManagementController(core.module.Base):
    update_rate = 10
    window = use_module('WindowRainManagement')
    door = use_module('DoorRainManagement')
    class Controller(core.fields.Base):
        def always(self):
           if window.Management() = 'RAIN'
                window.Management('CLOSE')
           else:
                window.Management('OPEN')
           if door.Management() = 'RAIN'
                door.Management('CLOSE')
           else:
                door.Management('OPEN')
