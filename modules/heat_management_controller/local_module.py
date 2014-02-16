import module
import fields
from module import use_module
import logging

class HeatManagementController(module.Base):
    update_rate = 10
    window = use_module('WindowHeatManagement')
    door = use_module('DoorHeatManagement')
    class controller(fields.Base):
        def __init__(self):
            self.temp_max = 40
            super(HeatManagementController.controller, self).__init__()
        def always(self):
            try:
                self.curr_win_management = self.module.window.management()[1]
                self.curr_door_management = self.module.door.management()[1]
		print "chaleur fenetre = %s / chaleur porte = %s" % (self.curr_win_management, self.curr_door_management)
                print "limite temp = %s" % (self.temp_max)
            except TypeError as e:
                logger = logging.getLogger()
                logger.exception(e)
            else:
                if self.curr_win_management > self.temp_max:
                    self.module.window.management(False)
                    print "la fenetre se ferme"
                else:
                    self.module.window.management(True)
                    print "la fenetre s'ouvre"
                if self.curr_door_management > self.temp_max:
                    self.module.door.management(False)
		    print "la porte se ferme"
                else:
                    self.module.door.management(True)
                    print "la porte s'ouvre"
