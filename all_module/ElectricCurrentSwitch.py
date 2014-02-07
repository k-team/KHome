from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class ElectricCurrentSwitch(core.module.Base):
    update_rate = 10
    room = use_module('Room')
    electricCurrentSensor = use_module('ElectricCurrentSensor')
    electricCurrentActuator = use_module('ElectricCurrentActuator')

    ElectricCurrentSwitch = fields.proxy.mix('ElectricCurrent',
                                       'ElectricCurrentSensor', 'ElectricCurrent',
                                   	   'ElectricCurrentActuator', 'ElectricCurrent')
