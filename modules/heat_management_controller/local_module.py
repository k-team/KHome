import module
import fields
import fields.io
import fields.persistant
import fields.proxy
import fields.sensor
import fields.actuator
from module import use_module

class HeatManagementController(core.module.Base):
    update_rate = 10
    temp_max = 40
    window = use_module('WindowHeatManagement')
    door = use_module('DoorHeatManagement')
    class controller(core.fields.Base):
        def _init_:
        temp_max = 40
        super(Controller, self)._init_
        def always(self):
            curr_win_management = window.Management()
            curr_door_management = door.Management()  
           if curr_win_management > temp_max:
                window.Management('CLOSE')
           else:
                window.Management('OPEN')
           if curr_door_management > temp_max:
                door.Management.('CLOSE')
           else:
                door.Management('OPEN')
