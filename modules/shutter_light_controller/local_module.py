import module
from module import use_module
import fields
import logging


class ShutterLightController(module.Base):
    update_rate = 500

    shutter = use_module('Shutter')
    luminosityInt = use_module('LuminosityInteriorSensor')
    luminosityExt = use_module('LuminosityExteriorSensor')
    presence = use_module('HumanPresenceSensor')
    
    class controller(fields.Base):
        
        def __init__(self):
            self.luminosity_limit = 60 # this represent the luminosity the user want in the room
            self.night_limit = 20 # this represent the luminosity limit to know if it is the night
            super(ShutterLightController.controller, self).__init__()
        
        def always(self):
            print "luminosity_limit = %s / night_limit = %s" % (self.luminosity_limit, self.night_limit)
            try:
                lumInt = self.module.luminosityInt.luminosity()[1]
                lumExt = self.module.luminosityExt.luminosity()[1]
                presence = self.module.presence.presence()[1]
                print "lumInt = %s / lumExt = %s / pres = %s" % (lumInt, lumExt, presence)
            except TypeError as e:
                logger = logging.getLogger()
                logger.exception(e)
            else:
                if  lumExt < self.night_limit:
                    #this represent he night (so we close the shutters)
                    print "close shutter because of night"
                    self.module.shutter.shutter(0)
                elif presence:
                    if lumInt < self.luminosity_limit :
                        if self.luminosity_limit < lumExt:
                           print "open shutter"
                           self.module.shutter.shutter(100)
