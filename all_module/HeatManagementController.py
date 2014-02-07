from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class HeatManagementController(core.module.Base):
    update_rate = 10
    TEMP_MAX = 40
    window = use_module('WindowHeatManagement')
    door = use_module('DoorHeatManagement')
    class Controller(core.fields.Base):
        def always(self):
           if window.Management() > TEMP_MAX
                window.Management('CLOSE')
           else:
                window.Management('OPEN')
           if door.Management() > TEMP_MAX
                door.Management.('CLOSE')
           else:
                door.Management('OPEN')
