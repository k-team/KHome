import module
import fields
import fields.io
import fields.sensor
import fields.persistant
import fields.syntax

class ElectricCurrentSensor(module.Base):
    update_rate = 10

    class electric_current(fields.syntax.Boolean,
            fields.sensor.ElectricCurrent, fields.io.Readable,
            fields.persistant.Volatile, fields.Base):
        pass
