# -*- coding: utf-8 -*-

import module
import fields
import socket
import json
import logging
import select

class NFC(module.Base):
    update_rate = 1
    public_name = 'NFC'
    nfc_sock = None

    def stop(self):
        if self.nfc_sock:
            self.nfc_sock.close()
        super(NFC, self).stop()

    class port(fields.io.Readable,
            fields.syntax.Integer,
            fields.persistant.Volatile,
            fields.Base):
        public_name = 'Port du capteur'
        init_value = 42420
        update_rate = 421337

    class host(fields.io.Readable,
            fields.io.Writable,
            fields.syntax.String,
            fields.persistant.Database,
            fields.Base):
        public_name = 'Adresse du capteur'
        update_rate = 421337

        def set_value(self, t, value):
            try:
                sock_tmp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock_tmp.connect((value, self.module.port()[1]))
            except socket.error as e:
                logging.exception(e)
                return False
            else:
                if self.module.nfc_sock is not None:
                    self.module.nfc_sock.close()
                self.module.nfc_sock = sock_tmp
                return super(NFC.host, self).set_value(t, value)

    class uid(fields.io.Readable,
            fields.syntax.String,
            fields.persistant.Database,
            fields.Base):
        public_name = 'UID'
        update_rate = 0.1
        sleep_on_start = 1

        def acquire_value(self):
            if self.module.nfc_sock is None:
                try:
                    host = self.module.host()[1]
                except TypeError:
                    return
                try:
                    sock_tmp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock_tmp.connect((host, self.module.port()[1]))
                except socket.error as e:
                    logging.exception(e)
                    return
                else:
                    self.module.nfc_sock = sock_tmp
            try:
                _, s, _ = select.select([], [self.module.nfc_sock], [], 1)
                if s:
                    s[0].send(json.dumps({ 'code': 'detected' }))
                    s, _, _ = select.select([self.module.nfc_sock], [], [], 1)
                    if s:
                        re = json.loads(s[0].recv(1024))
                        if not re['success']:
                            return
                        if not re['detected']:
                            return 'Pas de carte'
                        return re['uid']
            except (IOError, ValueError) as e:
                logging.exception(e)
