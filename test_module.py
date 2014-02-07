import os
import sys
import time
from twisted.internet import reactor

sys.path.append('core')
import fields
import fields.io
import fields.persistant
import fields.sensor
from module import Base, use_module

if __name__ == '__main__':
    class Module(Base):
        update_rate = 5

        class Field(
                fields.sensor.TemperaturSensor,
                fields.io.Readable,
                fields.io.Writable,
                fields.persistant.Volatile,
                fields.Base):
            pass

    b = Module()

    b.start()
    reactor.run()
    b.stop()
    b.join(1)
