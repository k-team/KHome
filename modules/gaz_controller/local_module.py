import module
import fields
from module import use_module

class GazController(module.Base):
    update_rate = 10
    co_gaz_security = use_module('COGazSecurity')
    kitchen_butane_gaz_security = use_module('KitchenButaneGazSecurity')
    kitchen_propane_gaz_security = use_module('KitchenPropaneGazSecurity')
    kitchen_methane_gaz_security = use_module('KitchenMethaneGazSecurity')
    class controller(fields.Base):
        def _init_:
            temp_max = 40
            #Les seuils ont été fixé suivant des valeurs réels
            co_value = 60
            propane_value = 1500
            butane_value = 1500
            methane_value = 1000
            super(GazController.controller, self)._init_
        def always(self):
            if self.module.co_gaz_security.gaz() > co_value:
                self.module.co_gaz_security.gaz('ALERT')
            if self.module.kitchen_propane_gaz_security.gaz() > propane_value:
                self.module.kitchen_propane_gaz_security.gaz('CLOSE')
            else:
                self.module.kitchen_propane_gaz_security.gaz('OPEN')
            if self.module.kitchen_butane_gaz_security.gaz() > butane_value:
                self.module.kitchen_butane_gaz_security.gaz('CLOSE')
            else:
                self.module.kitchen_butane_gaz_security.gaz('OPEN')
            if self.module.kitchen_methane_gaz_security.gaz() > methane_value:
                self.module.kitchen_methane_gaz_security.gaz('CLOSE')
            else:
                self.module.kitchen_methane_gaz_security.gaz('OPEN')
