from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class Temperature(core.module.Base):
    update_rate = 10
    salle = use_module('Salle')
    Temperature = fields.proxy.mix('Temperature',
                                   'TempCapteur', 'Temperature',
                                   'TempActionneur', 'Temperature')
