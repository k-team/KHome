from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

if __name__ == '__main__':

    class ChasseEau(core.module.Base):
        update_rate = 10
        actionneurPiston = use_module('ActionneurPiston')
        presencePersonne = use_module('PresencePersonne')

        Chasse = fields.proxy.mix('Chasse','ActionneurPiston', 'Piston', 'PresencePersonne', 'Presence')
        pass

