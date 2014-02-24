import module
import fields
import fields.io
import fields.syntax
import fields.persistant
import fields.actuator

class Alarm(module.Base):
    update_rate = 42000
    public_name = 'Alarme'

    class alarm(fields.io.Readable,
            fields.io.Writable,
            fields.syntax.Boolean,
            fields.persistant.Database,
            fields.Base):
        public_name = "Etat de l'alarme"

        def set_value(self, t, value):
            print 'Passage de l\'etat a', value
            if value == False:
                self.module.message('')
            return super(Alarm.alarm, self).set_value(t, value)

    class message(fields.io.Writable,
            fields.io.Readable,
            fields.syntax.String,
            fields.persistant.Database,
            fields.Base):
        public_name = "Message d'alerte"

        def set_value(self, t, value):
            print 'Passage du message a', value
            if value:
                self.module.alarm(True)
            return super(Alarm.message, self).set_value(t, value)
