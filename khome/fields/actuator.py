import sys
import logging
import socket

from khome.fields import io, syntax, persistant

logger = logging.getLogger()

def Dummy(data_type):
    """
    Dummy actuator, making a simply actuator.
    """
    class _Dummy(data_type, io.Writable):
        pass
    return _Dummy

Alarm = Dummy(syntax.Boolean)
Door = Dummy(syntax.Boolean)
ElectricCurrent = Dummy(syntax.Boolean)
Fan = Dummy(syntax.Boolean)
Butane = Dummy(syntax.Boolean) #true = ouvert, flase = ferme
Propane = Dummy(syntax.Boolean) #true = ouvert, flase = ferme
Methane = Dummy(syntax.Boolean) #true = ouvert, flase = ferme
LightButton = Dummy(syntax.Boolean)
Piston = Dummy(syntax.Boolean)
Shutter = Dummy(syntax.Percentage)
Temperature = Dummy(syntax.Numeric)
WaterValve = Dummy(syntax.Boolean)
Window = Dummy(syntax.Boolean)

class Actuator(io.Writable):
    host = '134.214.106.23'
    port = 5000

    def __init__(self):
        super(Actuator, self).__init__()
        self.actuator_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.actuator_socket.connect((type(self).host, type(self).port))
        self.actuator_socket_file = self.actuator_socket.makefile()

    def set_value(self, t, value):
        """
        Start the actuator (eg. start sending via the reactor).
        """
        logger.info('setting the value to %s', value)
        data = self.prepare_data(value)
        self.actuator_socket_file.write(data)
        self.actuator_socket_file.flush()
        return super(Actuator, self).set_value(t, value)

    def close(self):
        """
        Close/stop the actuator.
        """
        logger.info('closing the connection')
        self.actuator_socket_file.close()

    def prepare_data(self, data):
        """
        Format data to send to the actuator, depending on its needed format.
        """
        raise NotImplementedError

class PowerPlug(Actuator):
    actuator_id = 'FF9F1E05'
    org = '05'

    def prepare_data(self, data):
        data = '50000000' if data else  '70000000'
        return ''.join(('A55A6B', type(self).org, data,
            type(self).actuator_id, '308E'))
