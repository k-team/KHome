import fields.io
import fields.type

def Dummy(data_type):
    class _Dummy(data_type,
            fields.io.Writable):
        pass
    return _Dummy

TemperatureActuator = Dummy(fields.type.Numeric)
BoolActuator = Dummy(fields.type.Boolean)
StringActuator = Dummy(fields.type.String)
