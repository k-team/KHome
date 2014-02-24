#-*- coding: utf8 -*-
import module
from module import use_module
import fields
import fields.syntax
import fields.io


class MoistureReducing(module.Base):
    moisture_sensor = use_module('MoistureSensor')
    fan_actuator = use_module('FanActuator')

    #class moisture_value_limit(fields.syntax.Percentage, fields.io.Writable,
     #       fields.Base):
     #   pass

    class limit(
            fields.syntax.Percentage,
            fields.io.Writable,
            #fields.syntax.Constant,
            fields.syntax.Numeric,
            fields.Base):
        const_value = 45.0
        public_name = 'Humidité maximal autorisé'

    class controller(fields.Base):
        update_rate = 60 # update every minute

        #def __init__(self):
            #self.moisture_value_limit = 45 # moisture limit as a percentage
         #   super(MoistureReducing.controller, self).__init__()


        def always(self):
            """
            Reduce the moisture by checking the moisture level. If this one is over the
            """
            try:
                moisture_value = self.module.moisture_sensor.sensor()
                limit= self.module.limit
            except TypeError as e: # FIXME why TypeError ?
                #self.logger.exception(e)
                pass
            else:
                if moisture_value > limit:
                    self.module.fan_actuator.fan(True)
                    #self.logger.info('moisture (%s%) over limit, running fan',
                     #       moisture_value)
                    print 'moisture (%s%) over limit, running fan', moisture_value
                else:
                    self.module.fan_actuator.fan(False)
                    #self.logger.info('moisture (%s%) under limit, stopping fan',
                     #       moisture_value)
                    print 'moisture (%s%) under limit, stopping fan', moisture_value
