from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time

if __name__ == '__main__':
    class M1(core.module.Base):
        class Field(core.fields.io.Readable,
                core.fields.io.Writable,
                core.fields.persistant.Volatile,
                core.fields.Base):

            def _acquire_value(self):
                return (int(time.time()) % 10) ** 2

        class F1(core.fields.io.Readable,
                core.fields.io.Writable,
                core.fields.persistant.Volatile,
                core.fields.Base):
            pass

    b = M1()
    b.start()
    reactor.run()
    b.stop()
    b.join(1)
