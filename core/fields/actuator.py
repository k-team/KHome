import fields.io
import fields.type

def Dummy(data_type):
    class _Dummy(data_type,
            fields.io.Writable):
        pass
    return _Dummy

Alarm = Dummy(fields.type.Boolean)
Door = Dummy(fields.type.Boolean)
ElectricCurrent = Dummy(fileds.type.Boolean)
Fan = Dummy(fields.type.Boolean)
Gaz = Dummy(fields.type.Boolean)
LightButton = Dummy(fields.type.Boolean)
Piston = Dummy(fields.type.Boolean)
Shutter = Dummy(fields.type.Boolean)
Temperature = Dummy(fields.type.Numeric)
WaterValve = Dummy(fields.type.Boolean)
Window = Dummy(fields.type.Boolean)
