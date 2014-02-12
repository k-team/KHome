import module
import fields
import fields.io
import fields.persistant
import fields.proxy
import fields.sensor
import fields.actuator
from module import use_module

class RainManagementController(core.module.Base):
    update_rate = 10
    window = use_module('WindowRainManagement')
    door = use_module('DoorRainManagement')
    class controller(core.fields.Base):
        def always(self):
            curr_win_management = window.Management()
            curr_door_management = door.Management()    
            if curr_win_management == 'RAIN':
                window.Management('CLOSE')
            else:
                window.Management('OPEN')
            if curr_door_management == 'RAIN':
                door.Management('CLOSE')
            else:
                door.Management('OPEN')
