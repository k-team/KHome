import module
import fields

class COSensor(module.Base):
    update_rate = 10

    class value(fields.syntax.Numeric,
            fields.sensor.CO,
            fields.io.Graphable,
            fields.persistant.Database,
            fields.Base):
        public_name = 'Taux de CO (ppm)'

