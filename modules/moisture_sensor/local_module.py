import module
import fields
import fields.io
import fields.sensor
import fields.persistant
import fields.syntax
import logging

class MoistureSensor(module.Base):
    update_rate = 10

    class _moisture(fields.io.Hidden,fields.syntax.Numeric, fields.sensor.Moisture,
            fields.io.Readable, fields.persistant.Database, fields.Base):
        pass

  	class moisture(fields.io.Readable,
            fields.syntax.Numeric,
            fields.persistant.Volatile,
            fields.Base):
        sleep_on_start = 1
        update_rate = 0.1

        def acquire_value(self):
            try:
                v = int(self.module._moisture()[1])
                return v
            except TypeError as e:
                logging.exception(e)
                return