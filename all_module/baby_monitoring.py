from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

if __name__ == '__main__':
    class SoundSensor(core.module.Base):
        update_rate = 10
        class Sound(
            core.fields.sensor.Sound
            core.fields.io.Readable,
            core.fields.Base):
        pass

    class BabyMonitoring(core.module.Base):
        update_rate = 10
        sonCapteur = use_module('SoundSensor')
        recognition = use_module('Recognition')
        alarmActuator = use_module('AlarmActuator')

        Baby = fields.proxy.mix('Baby','SoundSensor', 'Sound', 'Recognition', 'Recognize', 'AlarmActuator', 'Alarm')

