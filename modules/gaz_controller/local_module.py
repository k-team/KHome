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
        def __init__(self):
            self.temp_max = 40
            #Les seuils ont été fixé suivant des valeurs réels
            self.co_value = 60
            self.propane_value = 1500
            self.butane_value = 1500
            self.methane_value = 1000
            super(GazController.controller, self).__init__()
        def always(self):
            if self.module.co_gaz_security.gaz() > self.co_value:
                self.module.co_gaz_security.gaz('ALERT')
            if self.module.kitchen_propane_gaz_security.gaz() > self.propane_value:
                self.module.kitchen_propane_gaz_security.gaz('CLOSE')
            else:
                self.module.kitchen_propane_gaz_security.gaz('OPEN')
            if self.module.kitchen_butane_gaz_security.gaz() > self.butane_value:
                self.module.kitchen_butane_gaz_security.gaz('CLOSE')
            else:
                self.module.kitchen_butane_gaz_security.gaz('OPEN')
            if self.module.kitchen_methane_gaz_security.gaz() > self.methane_value:
                self.module.kitchen_methane_gaz_security.gaz('CLOSE')
            else:
                self.module.kitchen_methane_gaz_security.gaz('OPEN')
