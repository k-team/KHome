import module
import fields
import fields.io
import fields.sensor
import fields.persistant

class LightButtonSensor(module.Base):
    update_rate = 10

    class light_button(fields.sensor.LightButtonSensor, fields.io.Readable,
            fields.persistant.Volatile, fields.Base):
        pass
