# -*- coding: utf-8 -*-
import module
import fields
import fields.syntax
import fields.io
from module import use_module
import logging

class GazController(module.Base):
    public_name = 'Control sécurisé du gaz'
    update_rate = 10

    co_gaz = use_module('COSensor')
    butane_gaz = use_module('ButaneGaz')
    propane_gaz = use_module('PropaneGaz')
    methane_gaz = use_module('MethaneGaz')
    alarm = use_module('AlarmActuator')

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
        public_name = 'Limite de méthane'

    class controller(fields.Base):
        def always(self):
            try:
                co_value_limit = self.module.co_value_limit()[1]
                propane_value_limit = self.module.propane_value_limit()[1]
                butane_value_limit = self.module.butane_value_limit()[1]
                methane_value_limit = self.module.methane_value_limit()[1]

                co_value_current = self.module.co_gaz.co_presence()[1]
                print 'co_value_current = %s / co_value_limit = %s' % (co_value_current, co_value_limit)
                propane_value_current = self.module.propane_gaz.taux()[1]
                print 'propane_value_current = %s / propane_value_limit = %s' % (propane_value_current, propane_value_limit)
                butane_value_current = self.module.butane_gaz.taux()[1]
                print 'butane_value = %s / butane_value_limit = %s' % (butane_value_current, butane_value_limit)
                methane_value_current = self.module.methane_gaz.taux()[1]
                print 'methane_value = %s / methane_value_limit = %s' % (methane_value_current, methane_value_limit)
            except TypeError as e:
                logger = logging.getLogger()
                logger.exception(e)
            else:
                if co_value_current > co_value_limit:
                    self.module.alarm.alarm(True)
                    print 'Alert A lot of CO gaz in the house'
                if propane_value_current > propane_value_limit:
                    self.module.alarm.alarm(True)
                    self.module.propane_gaz.gaz_actuator(True)
                    print 'Propane gaz is closed'
                else:
                    self.module.propane_gaz.gaz_actuator(False)
                    print 'Propane gaz is opened'
                if butane_value_current > butane_value_limit:
                    self.module.alarm.alarm(True)
                    self.module.butane_gaz.gaz_actuator(True)
                    print 'Butane gaz is closed'
                else:
                    self.module.butane_gaz.gaz_actuator(False)
                    print 'Butane gaz is opened'
                if methane_value_current > methane_value_limit:
                    self.module.alarm.alarm(True)
                    self.module.methane_gaz.gaz_actuator(True)
                    print 'Methane gaz is closed'
                else:
                    self.module.methane_gaz.gaz_actuator(False)
                    print 'Methane gaz is opened'
