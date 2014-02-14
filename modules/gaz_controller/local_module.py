import module
import fields
from module import use_module

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
            self.co_value = 60
            self.propane_value = 1500
            self.butane_value = 1500
            self.methane_value = 1000
            super(GazController.controller, self).__init__()
            
        def always(self):
            #print 'test'
            #print 'co_value = %s / limit = %s' % (self.module.co_gaz_security.gaz()[1], self.co_value)
            #print 'propane_value = %s / limit = %s' % (self.module.kitchen_propane_gaz_security.gaz()[1],self.propane_value)
            #print 'butane_value = %s / limit = %s' % (self.module.kitchen_butane_gaz_security.gaz()[1], self.butane_value)
            #print 'methane_value = %s / limit = %s' % (self.module.kitchen_methane_gaz_security.gaz()[1], self.methane_value)
            
            if self.module.co_gaz_security.gaz()[1] > self.co_value:
                self.module.alarm_actuator.alarm(True)
                #print "alarme lance car CO"
            if self.module.kitchen_propane_gaz_security.gaz()[1] > self.propane_value:
                self.module.kitchen_propane_gaz_security.gaz(False)
                #print "ferme gaz propane"
            else:
                self.module.kitchen_propane_gaz_security.gaz(True)
                print "ouvrir gaz propane"
            if self.module.kitchen_butane_gaz_security.gaz()[1] > self.butane_value:
                self.module.kitchen_butane_gaz_security.gaz(False)
                #print "ferme gaz butane"
            else:
                self.module.kitchen_butane_gaz_security.gaz(True)
                #print "ouvrir gaz butane"
            if self.module.kitchen_methane_gaz_security.gaz()[1] > self.methane_value:
                self.module.kitchen_methane_gaz_security.gaz(False)
                #print "ferme gaz methane"
            else:
                self.module.kitchen_methane_gaz_security.gaz(True)
                #print "ouvrir gaz methane"
