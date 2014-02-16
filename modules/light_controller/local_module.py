import module
from module import use_module
import fields

class LightController(module.Base):
    update_rate = 5

    light = use_module('LightButton')
    presence = use_module('HumanPresenceSensor')
    luminosity = use_module('LuminosityInteriorSensor')

    class controller(fields.Base):
        def __init__(self):
            self.luminosity_limit = 60 # for the time being it will be a percentage
            super(LightController.controller, self).__init__()

        def always(self):
            try:
                current_presence = self.module.presence.presence()[1]
                current_lum = self.module.luminosity.luminosity()[1]
            except TypeError:
                pass # Ignore
            else:
                if  current_presence:
                    if  current_lum < self.luminosity_limit:
                        self.module.light.light_button(True)
                else:
                    self.module.light.light_button(False)
