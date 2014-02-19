import module
import fields
import fields.io
import fields.sensor
import fields.persistant
import fields.syntax

class AirSensor(module.Base):
    update_rate = 10
    public_name = 'Analyseur d\'air'

    class air(
            fields.syntax.Numeric,
            fields.sensor.Air,
            fields.io.Readable,
            fields.persistant.Volatile,
            fields.Base):
        pass
