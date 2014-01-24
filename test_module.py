from twisted.internet import reactor
import core.module
import core.fields
import core.fields.io
import core.fields.persistant
import time
# import fields.io
# import fields.persistant

if __name__ == '__main__':
    print core.module.__dict__
    print core.fields.__dict__
    class M1(core.module.Base):
        class Field(core.fields.io.Readable,
                core.fields.io.Writable,
                core.fields.persistant.Volatile,
                core.fields.Base):
            field_name = 'mon_nom'

            def _acquire_value(self):
                return (int(time.time()) % 10) ** 2

        class F1(core.fields.io.Readable,
                core.fields.io.Writable,
                core.fields.persistant.Volatile,
                core.fields.Base):
            pass

    a = M1(name='M0')
    b = M1()
    print b.mon_nom()
    print b.mon_nom(10)
    print b.mon_nom()
    print b.mon_nom(t=time.time())
    print b.mon_nom(fr=time.time() - 5, to=time.time())
    for i in xrange(10):
        b.mon_nom(i)
        time.sleep(0.1)

    print b.mon_nom(fr=time.time() - 0.5, to=time.time())
    print b.mon_nom()
    print b.mon_nom(fr=time.time() - 0.5, to=time.time())

    print b.F1(10)
    print b.F1()

    print a.mon_nom(fr=0, to=time.time())

    b.start()
    reactor.run()

    try:
        while True:
            print b.mon_nom()
            time.sleep(0.4)
    except KeyboardInterrupt:
        b.stop()
        b.join(1)
