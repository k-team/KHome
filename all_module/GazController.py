import module
import fields
import fields.io
import fields.persistant
import fields.proxy
import fields.sensor
import fields.actuator
from module import use_module

class GazController(core.module.Base):
    update_rate = 10
    CO_gaz_security = use_module('COGazSecurity')
    kitchen_butane_gaz_security = use_module('KitchenButaneGazSecurity')
    kitchen_propane_gaz_security = use_module('KitchenPropaneGazSecurity')
    kitchen_methane_gaz_security = use_module('KitchenMethaneGazSecurity')
    class controller(core.fields.Base):
        def _init_:
            temp_max = 40
            co_value = 100
            propane_value = 100
            butane_value = 100
            methane_value = 100
            super(Controller, self)._init_
        def always(self):
            if CO_gaz_security.Gaz() > co_value:
                CO_gaz_security.Gaz('ALERT')
            if kitchen_propane_gaz_security.Gaz() > propane_value:
                kitchen_propane_gaz_security.Gaz('CLOSE')
            else:
                kitchen_propane_gaz_security.Gaz('OPEN')
            if kitchen_butane_gaz_security.Gaz() > butane_value:
                kitchen_butane_gaz_security.Gaz('CLOSE')
            else:
                kitchen_butane_gaz_security.Gaz('OPEN')
            if kitchen_methane_gaz_security.Gaz() > methane_value:
            else:
                kitchen_methane_gaz_security.Gaz('OPEN')
