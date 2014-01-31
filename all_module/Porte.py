from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

if __name__ == '__main__':
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

