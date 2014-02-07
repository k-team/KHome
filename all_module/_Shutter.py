from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time
import all_modules.shutter

class Shutter(core.module.Base)
    update_rate = 10
    sc = use_module('ShutterSensor')
    sa = use_module('ShutterActuator')

    Shutter = fields.proxy.mix('Shutter',
                               'ShutterSensor','Shutter',
                               'ShutterActuator','Shutter')
