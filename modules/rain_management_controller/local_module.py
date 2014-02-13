import module
import fields
from module import use_module

class RainManagementController(module.Base):
    update_rate = 10
    window = use_module('WindowRainManagement')
    door = use_module('DoorRainManagement')

    class controller(fields.Base):

        def _init_:
            super(RainManagementController.controller, self)._init_

        def always(self):
            curr_win_management = self.module.window.Management()
            curr_door_management = self.module.door.Management()    
            if curr_win_management == 'RAIN':
                self.module.window.Management('CLOSE')
            else:
                self.module.window.Management('OPEN')
            if curr_door_management == 'RAIN':
                self.module.door.Management('CLOSE')
            else:
                self.module.door.Management('OPEN')
