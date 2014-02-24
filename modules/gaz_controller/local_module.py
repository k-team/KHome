# -*- coding: utf-8 -*-

import module
from module import use_module
import fields

class GazController(module.Base):
    public_name = 'Control du gaz'
    update_rate = 10

    co_gaz = use_module('COSensor')
    butane_gaz = use_module('ButaneGaz')
    propane_gaz = use_module('PropaneGaz')
    methane_gaz = use_module('MethaneGaz')
    alarm = use_module('Alarm')

    butane = fields.proxy.readable('butane', 'ButaneGaz', 'butane')
    methane = fields.proxy.readable('methane', 'MethaneGaz', 'methane')
    propane = fields.proxy.readable('propane', 'PropaneGaz', 'propane')
    co = fields.proxy.readable('value', 'COSensor', 'value')
    alarm = fields.proxy.readable('alarm', 'Alarm', 'alarm')
    message = fields.proxy.readable('message', 'Alarm', 'message')

    class co_value_limit(fields.syntax.Constant, fields.syntax.Numeric,
            fields.Base):
        const_value = 60.0
        public_name = 'Limite de CO'

    class propane_value_limit(fields.syntax.Constant, fields.syntax.Numeric,
            fields.Base):
        const_value = 1500.0
        public_name = 'Limite de propane'

    class butane_value_limit(fields.syntax.Constant, fields.syntax.Numeric,
            fields.Base):
        const_value = 1400.0
        public_name = 'Limite de butane'

    class methane_value_limit(fields.syntax.Constant, fields.syntax.Numeric,
            fields.Base):
        const_value = 1600.0
        public_name = 'Limite de méthane'

    class controller(fields.Base):
        def always(self):
            try:
                co_value_limit = self.module.co_value_limit()[1]
                propane_value_limit = self.module.propane_value_limit()[1]
                butane_value_limit = self.module.butane_value_limit()[1]
                methane_value_limit = self.module.methane_value_limit()[1]

                co_value_current = self.module.co_gaz.value()[1]
                propane_value_current = self.module.propane_gaz.propane()[1]
                butane_value_current = self.module.butane_gaz.butane()[1]
                methane_value_current = self.module.methane_gaz.methane()[1]
            except TypeError as e:
                self.module.logger.exception(e)
            else:
                if co_value_current > co_value_limit:
                    self.module.alarm.alarm(True)
                    self.module.alarm.message('Too much CO gaz in the house')
                if propane_value_current > propane_value_limit:
                    self.module.alarm.alarm(True)
                    self.module.propane_gaz.gaz_actuator(True)
                    self.module.alarm.message('Too much propane gaz in the house')
                if butane_value_current > butane_value_limit:
                    self.module.alarm.alarm(True)
                    self.module.butane_gaz.gaz_actuator(True)
                    self.module.alarm.message('Too much butane gaz in the house')
                if methane_value_current > methane_value_limit:
                    self.module.alarm.alarm(True)
                    self.module.methane_gaz.gaz_actuator(True)
                    self.module.alarm.message('Too much methane gaz in the house')
