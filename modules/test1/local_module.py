import module
import fields
import fields.io
import fields.syntax
import fields.persistant

class Test1(module.Base):
    class field(
            fields.syntax.Numeric,
            fields.io.Readable,
            fields.persistant.Volatile,
            fields.Base):
        def acquire_value(self):
            return -42
