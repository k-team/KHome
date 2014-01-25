import json
from twisted.internet import protocol

class Protocol(protocol.Protocol):
    def __init__(self, module):
        self.module = module

    def dataReceived(self, data):
        print 'Reception des donnees :', data
        if not self.module.running:
            return

        try:
            json_data = json.loads(data)
        except ValueError:
            self.err_decode_data()
            return

        print 'json :', json_data
        if not 'code' in json_data:
            self.err_code_not_found()
            return

        code = str(json_data['code'])
        print 'code :', code
        if code == 'get_cur':
            self.get_cur(json_data)
        elif code == 'get_at':
            self.get_at(json_data)
        elif code == 'get_from_to':
            self.get_from_to(json_data)
        elif code == 'answer': # TODO
            self.load_answer(json_data)
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

    def err_field_error(self):
        self.error('Field not found')

    def get_cur(self, data):
        print 'get_cur'
        try:
            entry_objs = data['objs']
        except (TypeError, KeyError):
            self.err_decode_data()
            return
        print 'field :', entry_objs

        ls_attr = {}
        for attr in entry_objs:
            try:
                get = getattr(self.module, attr)
                ls_attr[attr] = get()
            except (AttributeError, IOError):
                self.err_field_error()
                return

        res = {}
        res['success'] = True
        res['objs'] = ls_attr
        print 'res :', res
        self.transport.write(json.dumps(res))

    def get_at(self, data):
        try:
            entry_objs = data['objs']
            t = float(data['time'])
        except (TypeError, KeyError):
            self.err_decode_data()
            return

        ls_attr = {}
        for attr in entry_objs:
            try:
                get = getattr(self.module, attr)
                ls_attr[attr] = get(t=t)
            except (AttributeError, IOError):
                self.err_field_error()
                return

        res = {}
        res['success'] = True
        res['objs'] = ls_attr
        self.transport.write(json.dumps(res))

    def get_from_to(self, data):
        try:
            entry_objs = data['objs']
            fr = float(data['time_begin'])
            to = float(data['time_end'])
        except (TypeError, KeyError):
            self.err_decode_data()
            return

        ls_attr = {}
        for attr in entry_objs:
            try:
                get = getattr(self.module, attr)
                ls_attr[attr] = get(fr=fr, to=to)
            except (AttributeError, IOError):
                self.err_field_error()
                return

        res = {}
        res['success'] = True
        res['objs'] = ls_attr
        self.transport.write(json.dumps(res))

class Factory(protocol.Factory):
    def __init__(self, module):
        self.module = module

    def buildProtocol(self, addr):
        return Protocol(self.module)
