import module
import fields
from module import use_module

class HeatManagementController(module.Base):
    update_rate = 10
    window = use_module('WindowHeatManagement')
    door = use_module('DoorHeatManagement')
    class controller(fields.Base):
        def __init__(self):
            self.temp_max = 40
            super(HeatManagementController.controller, self).__init__()
        def always(self):
            self.curr_win_management = self.module.window.management()
            self.curr_door_management = self.module.door.management()  
           if self.curr_win_management > self.temp_max:
                self.module.window.management('CLOSE')
           else:
                self.module.window.management('OPEN')
           if self.curr_door_management > self.temp_max:
                self.module.door.management.('CLOSE')
           else:
                self.module.door.management('OPEN')
