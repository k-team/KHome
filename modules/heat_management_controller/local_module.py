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
            self.temp_max = 30
            super(HeatManagementController.controller, self).__init__()
        def always(self):
            try:
                self.curr_win_temperature = self.module.window.temperature()[1]
                self.curr_door_temperature = self.module.door.temperature()[1]
		print "chaleur fenetre = %s / chaleur porte = %s" % (self.curr_win_temperature, self.curr_door_temperature)
                print "limite temp = %s" % (self.temp_max)
            except TypeError as e:
                logger = logging.getLogger()
                logger.exception(e)
            else:
                if self.curr_win_temperature > self.temp_max:
                    self.module.window.window_actuator(False)
                    print "la fenetre se ferme"
                else:
                    self.module.window.window_actuator(True)
                    print "la fenetre s'ouvre"
                if self.curr_door_temperature > self.temp_max:
                    self.module.door.door_actuator(False)
		    print "la porte se ferme"
                else:
                    self.module.door.door_actuator(True)
                    print "la porte s'ouvre"
