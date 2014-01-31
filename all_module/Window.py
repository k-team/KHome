from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

if __name__ == '__main__':
    class WindowSensor(core.module.Base):
        update_rate = 10
        class Window(
            core.fields.sensor.Window
            core.fields.io.Readable,
            core.fields.Base):
        pass

    class WindowActuator(core.module.Base):
        class Window(
            core.fields.actuator.Window
            core.fields.io.Writable,
            core.fields.Base):
        pass

    class WindowAcces(core.module.Base):
        update_rate = 10
        windowSensor = use_module('WindowSensor')
        windowActuator = use_module('WindowActuator')

        Window = fields.proxy.mix('Window', 'WindowSensor', 'Window', 'WindowActuator', 'Window')

