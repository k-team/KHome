import module
from module import use_module
import fields.proxy

class Recognition(module.Base):
    update_rate = 10
    camera_sensor = use_module('CameraSensor')

    recognised = fields.proxy.basic('recognised', 'CameraSensor', 'image')

    class RecognitionImage(module.Base):
        def acquire_value(self, who):
            pass
