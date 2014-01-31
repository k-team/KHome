from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class LuminositeExterieur(core.module.Base):
    update_rate = 10
    class Luminosite(
            core.fields.sensor.Lumiere,
            core.fields.io.Readable,
            core.fields.Base):
        pass
