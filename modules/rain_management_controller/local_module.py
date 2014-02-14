import module
import fields
from module import use_module

class RainManagementController(module.Base):
    update_rate = 10
    window = use_module('WindowRainManagement')
    door = use_module('DoorRainManagement')

    class controller(fields.Base):

        def always(self):
            curr_win_management = self.module.window.management()
            curr_door_management = self.module.door.management()    
            if curr_win_management == 'RAIN':
                self.module.window.management('CLOSE')
            else:
                self.module.window.management('OPEN')
            if curr_door_management == 'RAIN':
                self.module.door.management('CLOSE')
            else:
                self.module.door.management('OPEN')
