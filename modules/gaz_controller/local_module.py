import module
import fields
import fields.syntax
import fields.io
from module import use_module
import logging

class GazController(module.Base):
    update_rate = 10
    co_gaz_security = use_module('COGazSecurity')
    kitchen_butane_gaz_security = use_module('KitchenButaneGazSecurity')
    kitchen_propane_gaz_security = use_module('KitchenPropaneGazSecurity')
    kitchen_methane_gaz_security = use_module('KitchenMethaneGazSecurity')

    class co_value_limit(
            fields.syntax.Constant,
            fields.syntax.Numeric,
            fields.Base):
        const_value = 60.0
        public_name = 'Limite de CO'

    class propane_value_limit(
            fields.syntax.Constant,
            fields.syntax.Numeric,
            fields.Base):
        const_value = 1500.0
        public_name = 'Limite de propane'

    class butane_value_limit(
            fields.syntax.Constant,
            fields.syntax.Numeric,
            fields.Base):
        const_value = 1500.0
        public_name = 'Limite de butane'

    class methane_value_limit(
            fields.syntax.Constant,
            fields.syntax.Numeric,
            fields.Base):
        const_value = 1500.0
        public_name = 'Limite de methane'

    class controller(fields.Base):
        def always(self):
            try:
                co_value_limit = self.module.co_value_limit()[1]
                propane_value_limit = self.module.propane_value_limit()[1]
                butane_value_limit = self.module.butane_value_limit()[1]
                methane_value_limit = self.module.methane_value_limit()[1]

                co_value_current = self.module.co_gaz_security.taux()[1]
                print 'co_value_current = %s / co_value_limit = %s' % (co_value_current, co_value_limit)
                propane_value_current = self.module.kitchen_propane_gaz_security.taux()[1]
                print 'propane_value_current = %s / propane_value_limit = %s' % (propane_value_current, propane_value_limit)
                butane_value_current = self.module.kitchen_butane_gaz_security.taux()[1]
                print 'butane_value = %s / butane_value_limit = %s' % (butane_value_current, butane_value_limit)
                methane_value_current = self.module.kitchen_methane_gaz_security.taux()[1]
                print 'methane_value = %s / methane_value_limit = %s' % (methane_value_current, methane_value_limit)
            except TypeError as e:
                logger = logging.getLogger()
                logger.exception(e)
            else:
                if co_value_current > co_value_limit:
                    self.module.co_gaz_security.alarm(True)
                    print 'Alert A lot of CO gaz in the house'
                if propane_value_current > propane_value_limit:
                    self.module.kitchen_propane_gaz_security.alarm(True)
		    self.module.kitchen_propane_gaz_security.gaz_actuator(True)
                    print 'Propane gaz is closed'
                else:
                    self.module.kitchen_propane_gaz_security.alarm(False)
		    self.module.kitchen_propane_gaz_security.gaz_actuator(False)
                    print 'Propane gaz is opened'
                if butane_value_current > butane_value_limit:
                    self.module.kitchen_butane_gaz_security.alarm(True)
		    self.module.kitchen_butane_gaz_security.gaz_actuator(True)
                    print 'Butane gaz is closed'
                else:
                    self.module.kitchen_butane_gaz_security.alarm(False)
		    self.module.kitchen_butane_gaz_security.gaz_actuator(False)
                    print 'Butane gaz is opened'
                if methane_value_current > methane_value_limit:
                    self.module.kitchen_methane_gaz_security.alarm(True)
		    self.module.kitchen_methane_gaz_security.gaz_actuator(True)
                    print 'Methane gaz is closed'
                else:
                    self.module.kitchen_methane_gaz_security.alarm(False)
		    self.module.kitchen_methane_gaz_security.gaz_actuator(False)
                    print 'Methane gaz is opened'
