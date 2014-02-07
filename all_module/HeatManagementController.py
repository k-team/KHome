from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class HeatManagementController(core.module.Base):
    update_rate = 10
    temp_max = 40
    window = use_module('WindowHeatManagement')
    door = use_module('DoorHeatManagement')
    class Controller(core.fields.Base):
        def _init_:
        temp_max = 40
        super(Controller, self)._init_
        def always(self):
           if window.Management() > temp_max
                window.Management('CLOSE')
           else:
                window.Management('OPEN')
           if door.Management() > temp_max
                door.Management.('CLOSE')
           else:
                door.Management('OPEN')
                
class GazController(core.module.Base):
    update_rate = 10
    CO_gaz_security = use_module('COGazSecurity')
    kitchen_butane_gaz_security = use_module('KitchenButaneGazSecurity')
    kitchen_propane_gaz_security = use_module('KitchenPropaneGazSecurity')
    kitchen_methane_gaz_security = use_module('KitchenMethaneGazSecurity')
    class Controller(core.fields.Base):
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
            if kitchen_propane_gaz_security.Gaz() > propane_value
                kitchen_propane_gaz_security.Gaz('CLOSE')
            else:
                kitchen_propane_gaz_security.Gaz('OPEN')
            if kitchen_butane_gaz_security.Gaz() > butane_value
                kitchen_butane_gaz_security.Gaz('CLOSE')
            else:
                kitchen_butane_gaz_security.Gaz('OPEN')
            if kitchen_methane_gaz_security.Gaz() > methane_value
            else:
                kitchen_methane_gaz_security.Gaz('OPEN')
