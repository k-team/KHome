from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class GestionPluieFenetre(core.module.Base):
    update_rate = 10
    Gestion = fields.proxy.mix('Gestion',
                                'PrevisionPluie', 'Pluie',
                                'FenetreAcces', 'Fenetre')
