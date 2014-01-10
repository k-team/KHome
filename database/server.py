#!/usr/bin/env python2.7

import sqlite3
import json
from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import UNIXServerEndpoint as ServerEndpoint

class Database(Protocol):
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def dataReceived(self, data):
# TODO manage errors
        try:
            json_data = json.loads(data)
        except ValueError:
            return

        if not 'code' in json_data:
            return
        if not 'module' in json_data:
            return

        code = json_data['code']
        table_name = json_data['module']
        fields = None
        if 'fields' in json_data:
            fields = json_data['fields']

        if code == 'install':
            if fields is None:
                return
            self.db_install(table_name, fields)
        elif code == 'uninstall':
            self._db_uninstall(table_name)
        elif code == 'add':
            if fields is None:
                return
            self.db_install(table_name, fields)
        elif code == 'get_at':
            if fields is None:
                return
            if not 'time' in json_data:
                return
            self.db_install(table_name, json_data['time'], fields)
        elif code == 'get_from_to':
            if fields is None:
                return
            if not 'time_from' in json_data:
                return
            if not 'time_to' in json_data:
                return
            self.db_install(table_name, json_data['time_from'],
                    json_data['time_to'], fields)
        else:
            return

    def db_install(self, table_name, fields):
# c = conn.cursor()
# c.execute('SELECT ...')
# conn.commit()
        pass

    def db_uninstall(self, table_name):
        pass

    def db_add(self, table_name, fields):
        pass

    def db_get_at(self, table_name, time, fields):
        pass

    def db_get_from_to(self, table_name, t_from, t_to, fields):
        pass

class DBFactory(Factory):
    def __init__(self, db_filename):
        self.db_filename = db_filename

    def startFactory(self):
        self.db_conn = sqlite3.connect(self.db_filename)

    def stopFactory(self):
        self.db_conn.close()

    def buildProtocol(self, addr):
        return Database(self.db_conn)

db_filename = 'scutu.db'

endpoint = ServerEndpoint(reactor, './scutu.sock')
endpoint.listen(DBFactory(db_filename))
reactor.run()
