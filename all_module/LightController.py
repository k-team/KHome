import module
from module import use_module
import fields

class LightController(module.Base):
    shutter = use_module('Shutter')
    light = use_module('LightButton')
    presence = use_module('HumanPresence')
    luminosity = use_module('LuminosityInteriorSensor')

    class Controller(fields.Base):
        def __init__(self):
            self.luminosity_limit = 60 # for the time being it will be a percentage
            super(Controller, self).__init__()

        def always(self):
            if presence.presence():
                if luminosity.luminosity < self.luminosity_limit:
                    light.LightButton(True)
            else:
                light.LightButton(False)
