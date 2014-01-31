from twisted.internet import reactor
import core.module
from core.module import use_module
import core.fields
import core.fields.io
import core.fields.persistant
import time

if __name__ == '__main__':
    class TempKelvin(core.module.Base):
        update_rate = 10

        class kelvin(
                # core.fields.sensor.Temperature,
                core.fields.io.Readable,
                core.fields.persistant.Volatile,
                core.fields.Base):
            pass

    class TempsKelvinFiltered(core.module.Base):
            class kelvin(
                core.fields.io.Readable,
                core.fields.persistant.Volatile,
                core.fields.Base):
                T = use_module('TempKelvin')

                def _acquire_value(self):
                    return T.kelvin() * 0.5 + T.kelvin(t=-1) * 0.5

    class TempCelcius(core.module.Base):
        update_rate = 10
        T = use_module('TempKelvinFiltered')

        class celcius(core.fields.io.Readable,
                # core.fields.io.Writable,
                core.fields.persistant.Volatile,
                core.fields.Base):

            def _acquire_value(self):
                return T.kelvin() + 273.15

        class Field1(core.fields.io.Readable,
                core.fields.io.Writable,
                core.fields.persistant.Volatile,
                core.fields.Base):
            pass

    b = TempCelcius()

    b.start()
    reactor.run()
    b.stop()
    b.join(1)
