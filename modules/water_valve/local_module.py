import module
import fields
import fields.sensor
import fields.io

class WaterValveSensor(module.Base):
    update_rate = 10
    
    class water_valve(
            fields.sensor.WaterValve,
            fields.io.Readable,
            fields.Base):
        pass
