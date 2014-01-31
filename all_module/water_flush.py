from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

if __name__ == '__main__':

    class WaterFlush(core.module.Base):
        update_rate = 10
        actionneurPiston = use_module('ActuatorPiston')
        presencePersonne = use_module('PersonnePresence')

        Flush = fields.proxy.mix('Flush','ActuatorPiston', 'Piston', 'PersonnePresence', 'Presence')
