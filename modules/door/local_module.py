import module
import fields
import fields.actuator
import fields.sensor
import fields.persistant

class Door(module.Base):
    public_name = 'Porte auto'
    update_rate = 10

    class state(fields.sensor.Contact, fields.actuator.Door,
            fields.persistant.Volatile, fields.Base):
        public_name = 'Etat de la porte'
