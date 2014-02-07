from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time
import all_modules.ElectricCurrent
import all_modules.HumanPresenceSensor

if __name__ == '__main__':
    class ElectricCurrentController(core.module.Base)
        electricCurrent = use_module('ElectricCurrentSwitch')
        humanPresence = use_module('HumanPresenceSensor')

        class Controller(core.fields.Base):

            def always(self):
                if humanPresence.Presence() :
                   electricCurrent.ElectricCurrentSwitch(true)
                else
                   electricCurrent.ElectricCurrentSwitch(false)
