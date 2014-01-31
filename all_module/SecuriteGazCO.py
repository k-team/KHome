from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class SecuriteGazCO(core.module.Base):
    update_rate = 10
    Gaz = fields.proxy.mix('Gaz',
                                'CapteurCO', 'PresenceCO',
                                'ActionneurAlarme', 'Alarme')
