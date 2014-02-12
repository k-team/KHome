from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time



class LuminosityExteriorSensor(core.module.Base):
    update_rate = 10

    NIGHTLIMIT = 20
    
    class Luminosity(
            core.fields.sensor.LuminosityExterior
            core.fields.io.Readable,
            core.fields.persistant.Volatile,
            core.fields.Base):
        pass
        