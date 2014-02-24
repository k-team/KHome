import module
import fields
import fields.io
import fields.actuator
import fields.persistant
import fields.syntax

class FanActuator(module.Base):
    update_rate = 10
    public_name = 'Ventilateur'

    class fan(
            fields.actuator.Fan,
            #fields.io.Writable,
            fields.io.Readable,
            fields.syntax.Boolean,
            fields.persistant.Volatile,
            fields.Base):
        public_name = 'Etat du ventilateur'
