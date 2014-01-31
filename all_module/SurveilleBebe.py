from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

if __name__ == '__main__':
    class SonCapteur(core.module.Base):
        update_rate = 10
        class Son(
            core.fields.sensor.Son
            core.fields.io.Readable,
            core.fields.Base):
        pass

    class SurveilleBebe(core.module.Base):
        update_rate = 10
        sonCapteur = use_module('SonCapteur')
        reconnaissance = use_module('Reconnaissance')
        actionneurAlarme = use_module('ActionneurAlarme')

        Bebe = fields.proxy.mix('Bebe','SonCapteur', 'Son', 'Reconnaissance', 'Reconnu', 'ActionneurAlarme', 'Alarme')
        pass

