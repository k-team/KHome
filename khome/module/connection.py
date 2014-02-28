import json
from twisted.internet import protocol

class Protocol(protocol.Protocol):
    """
    Module specific protocol. To communicate with an other module, connect to
    its socket and then use the following keywords. All communication are
    JSON formatted.

    All requests have the following format: { "code": <code>, ... }.

    * Get information about a module : *knockknock*

    Return a set of information. This set is dynamic and may contains some
    words depending on the construction of the module. At least, it contains
    the following entries:
        * name: the module's name (unique id, string)
        * fields:
            * name: the field's name (unique id, string)

    * Query the module's fields current values: *get*

    Send also the fields queried (list of field names). Return if the query was
    successful ('success' key), and the field values acquired as a field ->
    value dictionary, where value in a tuple (timestamp, actual-value).

    * Query the module's fields values at a certain time: *get-at*

    Same result as when querying the current values, but adds the extra 'time'
    entry for the time of the query.

    * Query the module's fields values inside a timeslice: *get_from_to*

    Same result as when querying the current values, but adds the extra 'time_from' and 'time_to'
    entries for the timeslice of the query.

    * Set a field's value: *set*

    Send the field's name (field_name) and value (field_value). Return if the
    query was successful ('success' key).
    """
    def __init__(self, module):
        self.module = module

    def dataReceived(self, data):
        if not self.module.running:
            return

        # decode json data
        try:
            json_data = json.loads(data)
        except ValueError:
            self.err_decode_data()
            return

        if not 'code' in json_data:
            self.err_code_not_found()
            return

        # interpret protocol message
        code = str(json_data['code'])
        if code == 'knockknock':
            self.knock_knock()
        elif code == 'get':
            self.get_value(json_data)
        elif code == 'get_at':
            self.get_at(json_data)
        elif code == 'get_from_to':
            self.get_from_to(json_data)
        elif code == 'set':
            self.set_value(json_data)
        else:
            self.err_code_not_found()

    def send_json(self, obj):
        """
        Send a json object through the transport.
        """
        #json.dump(obj, self.transport) # doesn't work
        self.transport.write(json.dumps(obj) + '\n')
        # self.transport.flush()

    def err(self, msg):
        """
        Main error handler, logging and outputting return status to transport.
        """
        print msg # TODO log errors *correctly*
        self.send_json({ 'success': False })

    def err_decode_data(self):
        """
        Error handler called when received data couldn't be decoded.
        """
        self.err('Impossible to decode the received data')

    def err_code_not_found(self):
        """
        Error handler called when the query code wasn't found.
        self.err('Code not found in the query')
        """

    def err_field_error(self):
        """
        Error handler called when the queried field couldn't be found.
        """
        self.err('Field not found')

    def knock_knock(self):
        """
        Send all informations about the module via transport
        """
        self.send_json(self.module.get_info())

    def set_value(self, data):
        """
        Handler called to set a named field's value.
        """

        # decode the field caracteristics
        try:
            field_name = data['field_name']
            field_value = data['field_value']
        except (TypeError, KeyError):
            return self.err_decode_data()

        # set the field's value
        try:
            value = getattr(self.module, field_name)(field_value)
        except (AttributeError, IOError):
            return self.err_field_error()
        self.send_json({ 'success': value })

    def get_value(self, data):
        """
        Handler for getting one or many fields' value(s).
        """
        try:
            fields_name = data['fields']
        except (TypeError, KeyError):
            return self.err_decode_data()

        fields_value = {}
        for field in fields_name:
            try:
                get = getattr(self.module, field)
                fields_value[field] = get()
            except (AttributeError, IOError):
                return self.err_field_error()

        self.send_json({ 'success': True, 'fields': fields_value })

    def get_at(self, data):
        """
        Handler for getting one or many fields' value(s) at a given time.
        """
        try:
            fields_name = data['fields']
            time_at = float(data['time'])
        except (TypeError, KeyError):
            return self.err_decode_data()

        fields_value = {}
        for field in fields_name:
            try:
                fields_value[field] = getattr(self.module, field)(t=time_at)
            except (AttributeError, IOError):
                return self.err_field_error()
        self.send_json({ 'success': True, 'fields': fields_value })

    def get_from_to(self, data):
        """
        Handler for getting one or many fields' value(s) in a certain interval.
        """
        try:
            fields_name = data['fields']
            time_from = float(data['time_from'])
            time_to = float(data['time_to'])
        except (TypeError, KeyError):
            return self.err_decode_data()

        fields_value = {}
        for field in fields_name:
            try:
                get = getattr(self.module, field)
                fields_value[field] = get(fr=time_from, to=time_to)
            except (AttributeError, IOError):
                return self.err_field_error()
        self.send_json({ 'success': True, 'fields': fields_value })

class Factory(protocol.Factory):
    """
    Factory for the module protocol.
    """
    def __init__(self, module):
        self.module = module

    def buildProtocol(self, addr):
        return Protocol(self.module)
