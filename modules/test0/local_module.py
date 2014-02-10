import module
import fields
import fields.io
import fields.syntax
import fields.persistant

class Test0(module.Base):
    class field(
            fields.io.Readable,
            fields.syntax.Numeric,
            fields.persistant.Volatile,
            fields.Base):
        def acquire_value(self):
            return 42
