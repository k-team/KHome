import module
import fields
import fields.io
import fields.sensor
import fields.persistant

class ButaneSensor (module.Base):
    update_rate = 10

    class butane_presence(fields.sensor.Butane, fields.io.Readable,
            fields.persistant.Volatile,
            fields.Base):
        pass
