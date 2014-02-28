# -*- coding: utf-8 -*-

import shlex
import time
import subprocess as sp
from khome import module, fields
import threading

class PushUp(module.Base):
    public_name = 'Faites des pompes !'
    nfc = module.use_module('NFC')
    update_rate = 10

    class amount(fields.syntax.Numeric, fields.io.Writable, fields.io.Readable,
                     fields.persistant.Database, fields.Base):
        init_value = 0

    class controller(fields.Base):
        update_rate = 0.4

        def on_start(self):
            self.nbr = 0
            return super(PushUp.controller, self).on_start()

        def always(self):
            door_state = self.module.nfc.uid()[1] != 'Pas de carte'
            old = self.module.nfc.uid(t=-1)[1] != 'Pas de carte'
            self.module.logger.info('door state: %s', door_state)
            if door_state and not old:
                self.nbr += 1
                t = threading.Thread(target=self.play_music)
                t.start()
                time.sleep(1)
            return super(PushUp.controller, self).always()

        def play_music(self):
            try:
                fname = 'music/%s.wma' % (self.nbr % 2)
                self.module.logger.info('playing music %s', fname)
                cmd = 'mplayer -quiet -vo null -softvol -nolirc %s' % fname
                proc = sp.Popen(shlex.split(cmd))
                proc.wait()
            except (TypeError, sp.CalledProcessError) as e:
                self.module.logger.exception(e)
