import module
import fields
import fields.io
import fields.sensor
import fields.persistant
import fields.syntax

class LuminosityExteriorSensor(module.Base):
    update_rate = 10
    public_name = 'Capteur luminosite exterieure'

    class luminosity_exterior(
            fields.syntax.Numeric,
            fields.sensor.LuminosityExterior,
            fields.io.Graphable,
            fields.persistant.Volatile,
            fields.Base):
        public_name = 'Luminosite exterieure'
