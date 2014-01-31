from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

if __name__ == '__main__':

    class SecuritePorte(core.module.Base):
        update_rate = 10
        porteAcces = use_module('PorteAcces')
        reconnaissance = use_module('Reconnaissance')
        actionneurAlarme = use_module('ActionneurAlarme')

        Securite = fields.proxy.mix('Securite','PorteAcces', 'Porte', 'ActionneurAlarme', 'Alarme')
        pass