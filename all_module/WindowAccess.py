from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class WindowAccess(core.module.Base):
    update_rate = 10
    windowSensor = use_module('WindowSensor')
    windowActuator = use_module('WindowActuator')

    Window = fields.proxy.mix('Window', 
                              'WindowSensor', 'Window', 
                              'WindowActuator', 'Window')
