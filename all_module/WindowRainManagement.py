from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class WindowRainManagement(core.module.Base):
    update_rate = 10
    Management = fields.proxy.mix('Management',
                                	'RainForecast', 'Rain',
                                	'WindowAccess', 'Window')
    