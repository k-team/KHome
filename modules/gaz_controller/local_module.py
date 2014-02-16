import module
import fields
from module import use_module
import logging

class GazController(module.Base):
    update_rate = 10
    co_gaz_security = use_module('COGazSecurity')
    kitchen_butane_gaz_security = use_module('KitchenButaneGazSecurity')
    kitchen_propane_gaz_security = use_module('KitchenPropaneGazSecurity')
    kitchen_methane_gaz_security = use_module('KitchenMethaneGazSecurity')
    alarm_actuator = use_module('AlarmActuator')
    
    class controller(fields.Base):
        def __init__(self):
            self.temp_max = 40
            #Les seuils ont ete fixes suivant des valeurs reels
            self.co_value_limit = 60
            self.propane_value_limit = 1500
            self.butane_value_limit = 1500
            self.methane_value_limit = 1000
            super(GazController.controller, self).__init__()
            
        def always(self):
            print 'testons'
            try:
                co_value_current = self.module.co_gaz_security.gaz()[1]
                print 'co_value_current = %s / co_value_limit = %s' % (co_value_current, self.co_value_limit)
                propane_value_current = self.module.propane_gaz_security.gaz()[1]
                print 'propane_value_current = %s / propane_value_limit = %s' % (propane_value_current, self.propane_value_limit)
                butane_value_current = self.module.butane_gaz_security.gaz()[1]
                print 'butane_value = %s / butane_value_limit = %s' % (butane_value_current, self.butane_value_limit)
                methane_value_current = self.module.methane_gaz_security.gaz()[1]
                print 'methane_value = %s / methane_value_limit = %s' % (methane_value_current, self.methane_value_limit)
            except TypeError as e:
                logger = logging.getLogger()
                logger.exception(e)
            else:
                if co_value_current > self.co_value_limit:
                    self.module.alarm_actuator.alarm(True)
                    print 'Alert A lot of CO gaz in the house'
                if propane_value_current > self.propane_value_limit:
                    self.module.kitchen_propane_gaz_security.gaz(True)
                    print 'Propane gaz is closed'
                else:
                    self.module.kitchen_propane_gaz_security.gaz(False)
                    print 'Propane gaz is opened'
                if butane_value_current > self.butane_value_limit:
                    self.module.kitchen_butane_gaz_security.gaz(True)
                    print 'Butane gaz is closed'
                else:
                    self.module.kitchen_butane_gaz_security.gaz(False)
                    print 'Butane gaz is opened'
                if methane_value_current > self.methane_value_limit:
                    self.module.kitchen_methane_gaz_security.gaz(True)
                    print 'Methane gaz is closed'
                else:
                    self.module.kitchen_methane_gaz_security.gaz(False)
                    print 'Methane gaz is opened'
