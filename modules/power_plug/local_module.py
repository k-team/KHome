import module
import fields
import fields.io
import fields.persistant
import fields.actuator
import fields.syntax

class PowerPlug(module.Base):
    class plug(fields.actuator.PowerPlug, fields.syntax.Boolean,
            fields.persistant.Volatile, fields.Base):
        pass
