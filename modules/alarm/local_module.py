import module
import fields
import fields.io
import fields.syntax
import fields.persistant
import fields.actuator

class Alarm(module.Base):
    update_rate = 42000
    public_name = 'Alarme'

    class alarm(fields.actuator.Alarm,
            fields.persistant.Database,
            fields.Base):
        public_name = "Etat de l'alarme"

        def set_value(self, t, value):
            if value == False:
                self.module.message('')
            return super(Alarm.alarm, self).set_value(t, value)

    class message(fields.syntax.String,
            fields.io.Writable,
            fields.persistant.Database,
            fields.Base):
        public_name = "Message d'alerte"

        def set_value(self, t, value):
            if value:
                self.module.alarme(True)
            return super(Alarm.message, self).set_value(t, value)
