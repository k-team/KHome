import module
import fields
import fields.io
import fields.sensor
import fields.persistant

class PropaneSensor(module.Base):
    update_rate = 10

    class propane_presence(fields.sensor.Propane, fields.io.Readable,  fields.persistant.Volatile, fields.Base):
        pass
