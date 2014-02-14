import fields.io
import fields.syntax

def Dummy(data_type):
    class _Dummy(data_type,
            fields.io.Writable):
        pass
    return _Dummy

Alarm = Dummy(fields.syntax.Boolean)
Door = Dummy(fields.syntax.Boolean)
ElectricCurrent = Dummy(fields.syntax.Boolean)
Fan = Dummy(fields.syntax.Boolean)
Gaz = Dummy(fields.syntax.Boolean)
LightButton = Dummy(fields.syntax.Boolean)
Piston = Dummy(fields.syntax.Boolean)
Shutter = Dummy(fields.syntax.Boolean)
Temperature = Dummy(fields.syntax.Numeric)
WaterValve = Dummy(fields.syntax.Boolean)
Window = Dummy(fields.syntax.Boolean)
