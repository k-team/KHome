import module
import fields
import fields.io
import fields.actuator

class Alarm(module.Base):
    update_rate = 10000
    public_name = 'Alarme'

    class alarm(fields.actuator.Alarm,
            fields.Base):
        public_name = "Etat de l'alarme"
