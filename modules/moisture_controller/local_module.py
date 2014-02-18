import module
from module import use_module
import fields
import logging

class MoistureController(module.Base):
    update_rate = 10
    moisture_sensor = use_module('MoistureSensor')
    fan_actuator = use_module('FanActuator')
    class controller(fields.Base):

        def __init__(self):
            self.moisture_value_limit = 45 #faut le considerer en pourcentage
            super(MoistureController.controller, self).__init__()

        def always(self):
            print 'testons'
            try:
                moisture_value = self.module.moisture_sensor.moisture()
                print 'moisture_value = %s, moisture_value_limit = %s' % (moisture_value, self.moisture_value_limit)
            except TypeError as e:
                logger = logging.getLogger()
                logger.exception(e)
            else:
                if moisture_value > self.moisture_value_limit:
                    self.module.fan_actuator.fan(True)
                    print 'Run the fan'
                else:
                    self.module.fan_actuator.fan(False)
                    print 'Stop the fan'
