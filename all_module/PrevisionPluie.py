from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class PrevisionPluie(core.module.Base):
    update_rate = 10
    class Pluie(
            core.fields.sensor.PrevisionPluie,
            core.fields.io.Readable,
            core.fields.Base)
