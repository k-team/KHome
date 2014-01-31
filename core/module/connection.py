import json
from twisted.internet import protocol

class Protocol(protocol.Protocol):
    def __init__(self, module):
        self.module = module

    def dataReceived(self, data):
        if not self.module.running:
            return

        try:
            json_data = json.loads(data)
        except ValueError:
            self.err_decode_data()
            return

        if not 'code' in json_data:
            self.err_code_not_found()
            return

        code = str(json_data['code'])
        if code == 'get':
            self.get_value(json_data)
        elif code == 'get_at':
            self.get_at(json_data)
        elif code == 'get_from_to':
            self.get_from_to(json_data)
        elif code == 'set':
            self.set_value(json_data)
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

    def set_value(self, data):
        try:
            field_name = data['field_name']
            field_value = data['field_value']
        except (TypeError, KeyError):
            self.err_decode_data()
            return

        try:
            f_set = getattr(self.module, field_name)
            re = f_set(field_value)
        except (AttributeError, IOError):
            self.err_field_error()
            return

        res = {}
        res['success'] = re
        self.transport.write(json.dumps(res))

    def get_value(self, data):
        try:
            fields_name = data['fields']
        except (TypeError, KeyError):
            self.err_decode_data()
            return

        fields_value = {}
        for field in fields_name:
            try:
                get = getattr(self.module, field)
                fields_value[field] = get()
            except (AttributeError, IOError):
                self.err_field_error()
                return

        res = {}
        res['success'] = True
        res['objs'] = fields_value
        self.transport.write(json.dumps(res))

    def get_at(self, data):
        try:
            fields_name = data['fields']
            time_at = float(data['time'])
        except (TypeError, KeyError):
            self.err_decode_data()
            return

        fields_value = {}
        for field in fields_name:
            try:
                get = getattr(self.module, field)
                fields_value[field] = get(t=time_at)
            except (AttributeError, IOError):
                self.err_field_error()
                return

        res = {}
        res['success'] = True
        res['objs'] = fields_value
        self.transport.write(json.dumps(res))

    def get_from_to(self, data):
        try:
            fields_name = data['fields']
            time_from = float(data['time_from'])
            time_to = float(data['time_to'])
        except (TypeError, KeyError):
            self.err_decode_data()
            return

        fields_value = {}
        for field in fields_name:
            try:
                get = getattr(self.module, field)
                fields_value[field] = get(fr=time_from, to=time_to)
            except (AttributeError, IOError):
                self.err_field_error()
                return

        res = {}
        res['success'] = True
        res['objs'] = fields_value
        self.transport.write(json.dumps(res))

class Factory(protocol.Factory):
    def __init__(self, module):
        self.module = module

    def buildProtocol(self, addr):
        return Protocol(self.module)
