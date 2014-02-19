import module
import fields
import fields.io
import fields.actuator
import fields.persistant
import fields.syntax

class LightButtonActuator(module.Base):
    update_rate = 10

    class light_button(
            fields.actuator.LightButton,
            #idk the reason bu putting volatile get me a GTFO ...
            fields.Base):
        pass
