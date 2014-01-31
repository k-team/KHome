#!/usr/bin/env python2.7

import sqlite3 as lite
import json
from time import time
from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import UNIXServerEndpoint as ServerEndpoint

class Interpretor(Protocole):
    def __init__(self, module_source):
        self.module_source = module_source

    def receivedData(self, data):
        try:
            json_data = json.loads(data)
        except ValueError:
            self.err_decode_data()
            return

        if not 'cmd_type' in json_data:
            self.err_code_not_found()
            return
        if not 'objs' in json_data:
            self.err_code_not_found()
            return

        code = str(json_data['cmd_type'])
        
        if code == 'get_at':
            self.get_at(json_data)
        elif code == 'get_cur':
            self.get_cur()
        elif code == 'get_from_to':
            self.get_from_to(json_data)
        else:
            self.err_code_not_found()

    def error(self, msg):
# TODO log errors
        print(msg)
        re = {'success': False}
        self.transport.write(json.dumps(re))

    def err_decode_data(self):
        self.error('Impossible to decode the received data')

    def err_code_not_found(self):
        self.error('Code not found in the request')

    def err_arg_not_found(nom_argument):
        self.error(nom_argument + 'not found in the request !')

    """envoie d'un json a l'interpreteur qui l'a contacte"""
    def send(self, out):
        out_json = json.dumps(out)
        self.transport.write(out_json)
        
        
    def get_at(data):
        try:
            time_at = float(data['time_start'])
        except (KeyError, TypeError):
            self.err_code_arg_not_found('time_at');
            return
        try:
            arg_asked = data['obj']
        except (KeyError, TypeError):
            self.err_code_arg_not_found('objs');
            return
            objs = [len(arg_asked)]
            for i in range(len(obj)):
                answer = {}
                arg = module_source.getArg(arg_asked[i])
                answer['name'] = arg.name
                answer['type'] = arg.type
                obj_data = []
                obj_data_in = {}
                obj_data_in['time'], obj_data_in['value'] = arg.get_at(time_at);
                obj_data.append(obj_data_in)
                answer['obj_data'] = obj_data
                objs[i] = answer
            send(objs)

    def get_cur():
        try:
            arg_asked = data['obj']
        except (KeyError, TypeError):
            self.err_code_arg_not_found('objs');
            return
            objs = [len(arg_asked)]
            for i in range(len(obj)):
                answer = {}
                arg = module_source.getArg(arg_asked[i])
                answer['name'] = arg.name
                answer['type'] = arg.type
                obj_data = []
                obj_data_in = {}
                obj_data_in['time'], obj_data_in['value'] = arg.get_cur();
                obj_data.append(obj_data_in)
                answer['obj_data'] = obj_data
                objs[i] = answer
            send(objs)

    def get_from_to(data):
        try:
            time_start = float(data['time_start'])
        except (KeyError, TypeError):
            self.err_code_arg_not_found('time_start');
            return
        try:
            time_end = float(data['time_end'])
        except (KeyError, TypeError):
            self.err_code_arg_not_found('time_end');
            return
        try:
            arg_asked = data['obj']
        except (KeyError, TypeError):
            self.err_code_arg_not_found('objs');
            return
            objs = [len(arg_asked)]
            for i in range(len(obj)):
                answer = {}
                arg = module_source.getArg(arg_asked[i])
                answer['name'] = arg.name
                answer['type'] = arg.type
                obj_data = []
                liste_tuple = arg.get_from_to(time_start, time_end)
                for t_tuple in liste_tuple:
                    obj_data_in = {}
                    obj_data_in['time'], obj_data_in['value'] = t_tuple;
                    obj_data.appnd(obj_data_in)
                answer['obj_data'] = obj_data
                objs[i] = answer
            send(objs)

        

""" ? """
if __name__ == '__main__':
    factory = Factory()
    factory.protocol = Interpretor
    port = reactor.listenUNIX('module.sock', factory)
    reactor.run()

