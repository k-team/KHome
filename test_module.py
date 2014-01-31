from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

if __name__ == '__main__':
    class TempKelvin(core.module.Base):
        update_rate = 10

        class kelvin(
                core.fields.sensor.Temperature
                core.fields.io.Readable,
                core.fields.persistant.Volatile,
                core.fields.Base):
            pass

    class TempsKelvinFiltered(
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

    class PorteCapteur(core.module.Base):
        update_rate = 10
        class porte(
            core.fields.sensor.Porte
            core.fields.io.Readable,
            core.fields.Base):
        pass

    class PorteActionneur(core.module.Base):
        class porte(
            core.fields.actuator.Porte
            core.fields.io.Writable,
            core.fields.Base):
        pass

    class PorteAcces(core.module.Base):
        update_rate = 10
        porteCapteur = use_module('PorteCapteur')
        porteActionneur = use_module('PorteActionneur')

        porte = fields.proxy.mix('PorteCapteur', 'porte', 'PorteActionneur', 'porte')

        class Field(core.fields.proxy, core.fields.Base):
            proxy_module_name = "PorteCapteur"
            proxy_field_name = "porte"

        pass

    b = M1()

    b.start()
    reactor.run()
    b.stop()
    b.join(1)
