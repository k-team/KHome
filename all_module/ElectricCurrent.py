from twisted.internet import reactor
import module
import fields
import fields.io
import fields.persistant
import time

class ElectricCurrent(module.Base):
    update_rate = 10
    room = use_module('Room')
    ElectricCurrent = fields.proxy.mix('ElectricCurrent',
                                   		 'ElectricCurrentSensor', 'ElectricCurrent',
                                   		 'ElectricCurrentActuator', 'ElectricCurrent')
