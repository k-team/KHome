import module
import fields
from module import use_module
import logging

class RainManagementController(module.Base):
    update_rate = 10
    window = use_module('WindowActuator')
    door = use_module('DoorActuator')
    rain = use_module('RainForecast')

    class controller(fields.Base):

        def always(self):
            try:
                is_rain = self.module.rain.rain()[1]
                print "il pleut = %s" % is_rain
            except TypeError as e:
                logger = logging.getLogger()
                logger.exception(e)
            else:
                if is_rain:
                    print "on ferme volet et porte"
                    self.module.window.window(False)#on ferme les volets
                    self.module.door.door(False)#on ferme les portes
