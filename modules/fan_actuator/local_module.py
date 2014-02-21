import module
import fields
import fields.io
import fields.actuator

class FanActuator(module.Base):
    update_rate = 10
    public_name = 'Ventilateur'

    class fan(
            fields.actuator.Fan,
            fields.io.Writable,
            fields.Base):
        public_name = 'Etat du ventilateur'
