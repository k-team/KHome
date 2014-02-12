import module
import fields
import fields.io
import fields.sensor

class PropaneSensor(module.Base):
    update_rate = 10

    class propane_presence(fields.sensor.PropanePresence, fields.io.Readable, fields.Base):
        pass
