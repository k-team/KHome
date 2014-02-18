import module
import fields
import fields.io
import fields.sensor
import fields.persistant
import fields.syntax

class LightButtonSensor(module.Base):
    update_rate = 10

    class light_button(
            fields.syntax.Boolean, 
            fields.sensor.LightButton, 
            fields.io.Readable,
            fields.persistant.Volatile, 
            fields.Base):
        pass
