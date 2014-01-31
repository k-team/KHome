from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

if __name__ == '__main__':
    class PorteCapteur(core.module.Base):
        update_rate = 10
        class Porte(
            core.fields.sensor.Porte
            core.fields.io.Readable,
            core.fields.Base):
        pass

    class PorteActionneur(core.module.Base):
        class Porte(
            core.fields.actuator.Porte
            core.fields.io.Writable,
            core.fields.Base):
        pass

    class PorteAcces(core.module.Base):
        update_rate = 10
        porteCapteur = use_module('PorteCapteur')
        porteActionneur = use_module('PorteActionneur')

        Porte = fields.proxy.mix('Porte','PorteCapteur', 'Porte', 'PorteActionneur', 'Porte')
        pass

