from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time



class LuminosityInteriorSensor(core.module.Base):
    update_rate = 10

    
    class Luminosity(
            core.fields.sensor.LuminosityInterior
            core.fields.io.Readable,
            core.fields.persistant.Volatile,
            core.fields.Base):
        
        def _init_:
            luminosityLimit=60 # for the time being it will be a percentage. idk the real values
            super(Luminosity, self)._init_
        