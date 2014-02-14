import module
import fields
from module import use_module

class HeatManagementController(module.Base):
    update_rate = 10
    temp_max = 40
    window = use_module('WindowHeatManagement')
    door = use_module('DoorHeatManagement')
    class controller(fields.Base):
        def _init_:
            temp_max = 40
            super(HeatManagementController.controller, self)._init_
        def always(self):
            curr_win_management = self.module.window.management()
            curr_door_management = self.module.door.management()  
           if curr_win_management > temp_max:
                self.module.window.management('CLOSE')
           else:
                self.module.window.management('OPEN')
           if curr_door_management > temp_max:
                self.module.door.management.('CLOSE')
           else:
                self.module.door.management('OPEN')
