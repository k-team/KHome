import module
from module import use_module
import fields.proxy

class Recognition(module.Base):
    update_rate = 10
    camera_sensor = use_module('CameraSensor')

    recognised = fields.proxy.mix('Recognised', 'CameraSensor', 'Image')

    class RecognitionImage(module.Base):
        def _acquire_value(self, who):
            pass
