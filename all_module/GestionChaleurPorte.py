from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class GestionChaleurPorte(core.module.Base):
    update_rate = 10
    Gestion = fields.proxy.mix('Gestion',
                                'PrevisionTemp', 'Temperature',
                                'PorteAcces', 'Porte')
