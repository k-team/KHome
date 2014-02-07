import module
from module import use_module
import fields.proxy

class Recognition(module.Base)
    update_rate = 10

    CameraSensor = use_module('CameraSensor')

    recognised = fields.proxy.mix('Recognised', 'CameraSensor', 'Image')
