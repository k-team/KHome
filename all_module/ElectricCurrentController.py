from twisted.internet import reactor
import module
import fields
import fields.io
import fields.persistant
import time
import all_modules.electricCurrent

if __name__ == '__main__':
    class ElectricCurrentController(module.Base)
        electricCurrent = use_module('ElectricCurrent')
        humanPresence = use_module('HumanPresence')

        ElectricCurrentController = fields.proxy.mix('ElectricCurrentController',
                                   		 'ElectricCurrent', 'ElectricCurrent',
                                   		 'HumanPresence', 'Presence')
        def always(self):
            '''
            if electricCurrent != 0
							if humanPresence.Presence
								ShutDownTheElectricCurrentSwitch
							else
								do nothing
						'''
