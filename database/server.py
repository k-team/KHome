#!/usr/bin/env python2.7

import sqlite3 as lite
import json
from time import time
from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import UNIXServerEndpoint as ServerEndpoint

class Database(Protocol):
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def dataReceived(self, data):
        try:
            json_data = json.loads(data)
        except ValueError:
            self.err_decode_data()
            return

        if not 'code' in json_data:
            self.err_code_not_found()
            return

        code = str(json_data['code'])
        if code == 'install':
            self.db_install(json_data)
        elif code == 'uninstall':
            self.db_uninstall(json_data)
        elif code == 'add':
            self.db_add(json_data)
        elif code == 'get_at':
            self.db_get_at(json_data)
        elif code == 'get_from_to':
            self.db_get_from_to(json_data)
        else:
            self.err_code_not_found()

    def error(self, msg):
# TODO log errors
        print msg
        re = {'success': False}
        self.transport.write(json.dumps(re))

    def err_decode_data(self):
        self.error('Impossible to decode the received data')

    def err_code_not_found(self):
        self.error('Code not found in the query')

    def err_bad_query(self):
        self.error('Bad query')

    def err_db_error(self, msg):
        self.error('DB error: ' + msg)

    def sql_query(self, query, param=tuple(), get=False, commit=True):
        print 'query: ', query
        print 'param: ', param
        re = False
        try:
            c = self.db_conn.cursor()
            c.execute(query, param)
            if get:
                re = c.fetchall()
            if commit:
                self.db_conn.commit()
        except lite.Error as e:
            self.db_conn.rollback()
            self.err_db_error(str(e.args[0]))
            return False
        return re

    def db_install(self, data):
        db_types = {'numeric': 'real',
                'string': 'varchar(255)',
                'boolean': 'boolean'}

        try:
            table_name = str(data['module'])
            fields = data['fields']
            fields_s = [f['name'] + ' ' + db_types[f['type']] for f in fields]
        except (KeyError, TypeError):
            self.err_bad_query()
            return

        if not fields:
            self.err_bad_query()
            return

        query = 'CREATE TABLE %s (time real primary key, %s)' \
                % (table_name, ', '.join(fields_s))
        self.sql_query(query)

    def db_uninstall(self, data):
        try:
            table_name = str(data['module'])
        except KeyError:
            self.err_bad_query()
        else:
            query = 'DROP TABLE %s' % table_name
            self.sql_query(query)

    def db_add(self, data):
        try:
            table_name = str(data['module'])
            fields = data['fields']
            fields_name = [str(f['name']) for f in fields]
            fields_value = [str(f['value']) for f in fields]
        except (KeyError, TypeError):
            self.err_bad_query()
            return

        if not fields:
            self.err_bad_query()
            return

        query = 'INSERT INTO %s (time, %s) VALUES ("%s", %s)' \
                % (table_name, ', '.join(fields_name), time(),
                ', '.join('?' * len(fields_value)))
        self.sql_query(query, tuple(fields_value))

    def db_get_at(self, data):
        try:
            table_name = str(data['module'])
            fields = map(str, data['fields'])
            time_at = float(data['time_at'])
        except (KeyError, TypeError):
            self.err_bad_query()
            return

        if not fields:
            self.err_bad_query()
            return

        query = 'SELECT time, %s FROM %s \
                WHERE time < ? ORDER BY time DESC LIMIT 1' \
                % (', '.join(fields), table_name)
        result = self.sql_query(query, (time_at,), True)
        out = {'success': False}
        if result:
            out = {}
            out['success'] = True
            out['time'] = result[0][0]
            out['data'] = [{'name': n, 'value': v}
                    for n, v in zip(fields, result[0][1:])]
        out_json = json.dumps(out)
        print out_json
        self.transport.write(out_json)

    def db_get_from_to(self, data):
        try:
            table_name = str(data['module'])
            fields = map(str, data['fields'])
            time_from = float(data['time_from'])
            time_to = float(data['time_to'])
        except (KeyError, TypeError):
            self.err_bad_query()
            return

        if not fields:
            self.err_bad_query()
            return

        query = 'SELECT time, %s FROM %s \
                WHERE time < ?  AND time > ? ORDER BY time DESC' \
                % (', '.join(fields), table_name)
        result = self.sql_query(query, (time_to, time_from), True)
        out = {'success': False}
        if result:
            out = {}
            out['success'] = True
            out['data'] = [{'time': r[0], 'fields': [{'name': n, 'value': v}
                    for n, v in zip(fields, r[1:])]} for r in result]
        out_json = json.dumps(out)
        print out_json
        self.transport.write(out_json)

class DBFactory(Factory):
    def __init__(self, db_filename):
        self.db_filename = db_filename

    def startFactory(self):
        self.db_conn = lite.connect(self.db_filename)

    def stopFactory(self):
        self.db_conn.close()

    def buildProtocol(self, addr):
        return Database(self.db_conn)

db_filename = 'scutu.db'
endpoint = ServerEndpoint(reactor, './scutu.sock')
endpoint.listen(DBFactory(db_filename))
reactor.run()
