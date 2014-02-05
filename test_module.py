import os
import sys
import time
from twisted.internet import reactor

sys.path.append('core')
import fields
import fields.io
import fields.persistant
from module import Base, use_module

if __name__ == '__main__':
    # class TempKelvin(Base):
    #     update_rate = 10

    #     class kelvin(
    #             # fields.sensor.Temperature,
    #             fields.io.Readable,
    #             fields.persistant.Volatile,
    #             fields.Base):
    #         pass

    # class TempsKelvinFiltered(Base):
    #         class kelvin(
    #             fields.io.Readable,
    #             fields.persistant.Volatile,
    #             fields.Base):
    #             T = use_module('TempKelvin')

    #             def _acquire_value(self):
    #                 return T.kelvin() * 0.5 + T.kelvin(t=-1) * 0.5

    # class TempCelcius(Base):
    #     update_rate = 10
    #     T = use_module('TempKelvinFiltered')

    #     class celcius(fields.io.Readable,
    #             # fields.io.Writable,
    #             fields.persistant.Volatile,
    #             fields.Base):

    #         def _acquire_value(self):
    #             return T.kelvin() + 273.15

    #     class Field1(fields.io.Readable,
    #             fields.io.Writable,
    #             fields.persistant.Volatile,
    #             fields.Base):
    #         pass

    class Module(Base):
        update_rate = 5

        class Field(fields.io.Readable,
                fields.io.Writable,
                fields.persistant.Volatile,
                fields.Base):
            def acquire_value(self):
                return time.time() % 10

    b = Module()

    b.start()
    reactor.run()
    b.stop()
    b.join(1)
