import module
from module import use_module
import fields

class LightController(module.Base):
    light = use_module('LightButton')
    presence = use_module('HumanPresence')
    luminosity = use_module('LuminosityInteriorSensor')

    class controller(fields.Base):
        def _init_:
            luminosity_limit = 60 # for the time being it will be a percentage
            super(LightController.controller, self)._init_

        def always(self):
            if self.module.presence.presence():
                if self.module.luminosity.luminosity() < self.luminosity_limit:
                    self.module.light.light_button(True)
            else:
                self.module.light.light_button(False)
