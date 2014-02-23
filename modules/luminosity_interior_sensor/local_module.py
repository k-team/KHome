import module
import fields
import fields.io
import fields.sensor
import fields.persistant
import fields.syntax

class LuminosityInteriorSensor(module.Base):
    update_rate = 10
    public_name = 'Capteur luminosite interieure'

    class luminosity(
            fields.syntax.Numeric,
            fields.sensor.LuminosityInterior,
            # fields.io.Readable,
            fields.persistant.Volatile,
            fields.Base):
        public_name = 'Luminosite interieure'


