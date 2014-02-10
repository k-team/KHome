import module
from module import use_module
import fields
import fields.io
import fields.syntax
import fields.persistant

T0 = use_module('Test0')
T1 = use_module('Test1')

class Test2(module.Base):
    class field(
            fields.syntax.Numeric,
            fields.io.Readable,
            fields.persistant.Volatile,
            fields.Base):
        def acquire_value(self):
            return T0.field()[1] + T1.field()[1]
