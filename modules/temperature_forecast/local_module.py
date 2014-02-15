import module
import fields
import fields.io
import fields.sensor
import fields.persistant
import fields.syntax

class TemperatureForecast(module.Base):
    update_rate = 10

    class temperature(fields.syntax.Numeric, 	    	     		    fields.sensor.TemperatureForecast,
            fields.persistant.Volatile,
            fields.io.Readable,
            fields.Base):
        pass
