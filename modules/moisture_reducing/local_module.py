# -*- coding: utf8 -*-

import module
from module import use_module
import fields

class MoistureReducing(module.Base):
    public_name = 'Humidite automatique'

    moisture_sensor = use_module('MoistureSensor')
    fan_actuator = use_module('FanActuator')

    anonyme = fields.proxy.readable('sensor', 'MoistureSensor', 'sensor')
    anonyme2 = fields.proxy.basic('fan', 'FanActuator', 'fan')

    class limit(fields.syntax.Percentage, fields.io.Writable,
            fields.io.Readable, fields.syntax.Numeric,
            fields.persistant.Volatile, fields.Base):
        const_value = 45.0
        public_name = 'Humidité maximal autorisé'

    class controller(fields.Base):
        update_rate = 60 # update every minute

        def always(self):
            """
            Reduce the moisture by checking the moisture level. If this one is over the
            """
            logger = self.module.logger
            moisture_value = self.module.moisture_sensor.moisture()
            if moisture_value is None:
                return
            if moisture_value > self.moisture_value_limit:
                self.module.fan_actuator.fan(True)
                logger.info('moisture (%s%) over limit, running fan',
                        moisture_value)
            else:
                self.module.fan_actuator.fan(False)
                logger.info('moisture (%s%%) under limit, stopping fan',
                        moisture_value)
