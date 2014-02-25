# -*- coding: utf8 -*-

import module
from module import use_module
import fields

class MoistureReducing(module.Base):
    public_name = 'Humidite automatique'

    fan_actuator = use_module('FanActuator')
    moisture_sensor = use_module('MoistureSensor')

    moisture = fields.proxy.readable('moisture', 'MoistureSensor', 'sensor')
    fan = fields.proxy.readable('fan', 'FanActuator', 'fan')

    class moisture_value_limit(fields.syntax.Percentage, fields.io.Writable,
            fields.io.Readable, fields.syntax.Numeric,
            fields.persistant.Volatile, fields.Base):
        update_rate = 421337
        public_name = 'Humidité maximale autorisée'
        init_value = 45.0

    class controller(fields.Base):
        update_rate = 15 # update for half the sensor's time

        def always(self):
            logger = self.module.logger
            moisture_value = self.module.moisture_sensor.sensor()[1]
            moisture_value_limit = self.module.moisture_value_limit()[1]
            if moisture_value is None:
                return
            if moisture_value > moisture_value_limit:
                self.module.fan_actuator.fan(True)
                logger.info('moisture (%s %%) over limit (%s %%), running fan',
                        moisture_value, moisture_value_limit)
            else:
                self.module.fan_actuator.fan(False)
                logger.info('moisture (%s %%) under limit (%s %%), stopping fan',
                        moisture_value, moisture_value_limit)
