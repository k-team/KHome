import module
import fields
import fields.io
import fields.sensor

class DoorSensor(module.Base):
    update_rate = 10

    class door(fields.sensor.Door, fields.io.Readable, fields.Base):
        pass

