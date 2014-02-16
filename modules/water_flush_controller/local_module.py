import module
from module import use_module
import fields
import logging

class WaterFlushController(module.Base):
    update_reate = 10
    water_flush = use_module('WaterFlush')

    class controller(fields.Base):

        def __init__(self):
            self.presence_before = False
            super(WaterFlushController.controller, self).__init__()
        
        def always(self):
            print "testons"
            try:
		presence_now = self.module.water_flush.flush()[1]
	        print "presence_before = %s, presence_now = %s" % (self.presence_before, presence_now)
	    except TypeError as e:
                logger = logging.getLogger()
                logger.exception(e)
            else:
                if self.presence_before and not presence_now:#si il y avait quelqu'un devant, et qu'il est parti
                    self.module.water_flush.flush(True)#Tirer la chasse
                    print "la chasse est tiree"
                else:
                    self.module.water_flush.flush(False)#remettre le piston
                    print "la chasse n'est pas tiree"
		self.presence_before = presence_now
