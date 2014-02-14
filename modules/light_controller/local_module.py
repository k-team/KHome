import module
from module import use_module
import fields

class LightController(module.Base):
    update_rate = 5

    light = use_module('LightButton')
    presence = use_module('HumanPresence')
    luminosity = use_module('LuminosityInteriorSensor')

    class controller(fields.Base):
        def __init__(self):
            self.luminosity_limit = 60 # for the time being it will be a percentage
            super(controller, self).__init__()

        def always(self):
            if presence.presence():
                if luminosity.luminosity() < self.luminosity_limit:
                    light.light_button(True)
            else:
                light.light_button(False)
