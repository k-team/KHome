from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

if __name__ == '__main__':
    class FenetreCapteur(core.module.Base):
        update_rate = 10
        class fenetre(
            core.fields.sensor.Fenetre
            core.fields.io.Readable,
            core.fields.Base):
        pass

    class FenetreActionneur(core.module.Base):
        class fenetre(
            core.fields.actuator.Fenetre
            core.fields.io.Writable,
            core.fields.Base):
        pass

    class FenetreAcces(core.module.Base):
        update_rate = 10
        fenetreCapteur = use_module('FenetreCapteur')
        fenetreActionneur = use_module('FenetreActionneur')

        fenetre = fields.proxy.mix('FenetreCapteur', 'fenetre', 'FenetreActionneur', 'fenetre')

        class Field(core.fields.proxy, core.fields.Base):
            proxy_module_name = "FenetreCapteur"
            proxy_field_name = "fenetre"

        pass

