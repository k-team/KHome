import module
from module import use_module
import fields

class ShutterSecurityController(module.Base):
        update_rate = 2

        shutter = use_module('Shutter')
        presence = use_module('HumanPresenceSensor')


        class controller(fields.Base):
            def always(self):
                try:
                    pres = self.module.presence.presence()
                    print "presence = %s" % pres
                except TypeError:
                    pass # Ignore
                else:
                    if not pres[1] :
                        print "volet ferme"
                        self.module.shutter.shutter(0)
