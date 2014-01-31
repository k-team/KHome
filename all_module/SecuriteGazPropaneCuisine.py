from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class SecuriteGazPropaneCuisine(core.module.Base):
    update_rate = 10
    Alarme = fields.proxy.writable('Alarme', 'ActionneurAlarme', 'Alarme')
    Gaz = fields.proxy.mix('Gaz',
                                'CapteurPropane', 'PresencePropane',
                                'ActionneurGaz', 'Gaz')
