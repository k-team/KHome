from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class RainForecast(core.module.Base):
    update_rate = 10
    class Rain(
            core.fields.sensor.RainForecast,
            core.fields.io.Readable,
            core.fields.Base)
