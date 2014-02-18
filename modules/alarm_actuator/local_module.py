import module
import fields
import fields.io
import fields.actuator

class AlarmActuator(module.Base):
    update_rate = 10
    public_name = 'Alarme'

    class alarm(fields.actuator.Alarm, fields.io.Writable, fields.Base):
        pass
