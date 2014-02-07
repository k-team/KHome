from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

class WindowActuator(core.module.Base):
    update_rate = 10
    class Window(
            core.fields.actuator.Window
            core.fields.io.Writable,
            core.fields.Base)
