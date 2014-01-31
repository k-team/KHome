from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

if __name__ == '__main__':
    class FenetreCapteur(core.module.Base):
        update_rate = 10
        class Fenetre(
            core.fields.sensor.Fenetre
            core.fields.io.Readable,
            core.fields.Base):
        pass

    class FenetreActionneur(core.module.Base):
        class Fenetre(
            core.fields.actuator.Fenetre
            core.fields.io.Writable,
            core.fields.Base):
        pass

    class FenetreAcces(core.module.Base):
        update_rate = 10
        fenetreCapteur = use_module('FenetreCapteur')
        fenetreActionneur = use_module('FenetreActionneur')

        Fenetre = fields.proxy.mix('FenetreCapteur', 'Fenetre', 'FenetreActionneur', 'Fenetre')

        class Field(core.fields.proxy, core.fields.Base):
            proxy_module_name = "FenetreCapteur"
            proxy_field_name = "Fenetre"

        pass

