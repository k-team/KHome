import module
from module import use_module
import fields.proxy

class BabyMonitoring(module.Base):
    update_rate = 10

    SoundSensor = use_module('SoundSensor')
    Recognition = use_module('Recognition')
    AlarmActuator = use_module('AlarmActuator')

    baby = fields.proxy.mix('Baby', 'SoundSensor', 'Sound', 'Recognition',
            'Recognised', 'AlarmActuator', 'Alarm')
