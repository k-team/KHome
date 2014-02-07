from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class GazController(core.module.Base):
    update_rate = 10
    CO_VALUE = 100
    PROPANE_VALUE = 100
    BUTANE_VALUE = 100
    METHANE_VALUE = 100
    CO_gaz_security = use_module('COGazSecurity')
    kitchen_butane_gaz_security = use_module('KitchenButaneGazSecurity')
    kitchen_propane_gaz_security = use_module('KitchenPropaneGazSecurity')
    kitchen_methane_gaz_security = use_module('KitchenMethaneGazSecurity')
    class Controller(core.fields.Base):
        def always(self):
            if CO_gaz_security.Gaz() > CO_VALUE:
                CO_gaz_security.Gaz('ALERT')
            if kitchen_propane_gaz_security.Gaz() > PROPANE_VALUE
                kitchen_propane_gaz_security.Gaz('CLOSE')
            else:
                kitchen_propane_gaz_security.Gaz('OPEN')
            if kitchen_butane_gaz_security.Gaz() > BUTANE_VALUE
                kitchen_butane_gaz_security.Gaz('CLOSE')
            else:
                kitchen_butane_gaz_security.Gaz('OPEN')
            if kitchen_methane_gaz_security.Gaz() > METHANE_VALUE
            else:
                kitchen_methane_gaz_security.Gaz('OPEN')
