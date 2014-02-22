import module
import fields
import fields.actuator
import fields.sensor
import fields.persistant

class Window(module.Base):
    public_name = 'Fenetre auto'
    update_rate = 10

    class state(fields.sensor.Contact, fields.actuator.Window,
            fields.persistant.Volatile, fields.Base):
        public_name = 'Etat de la fenetre'
