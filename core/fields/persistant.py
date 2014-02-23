import sqlite3
import logging

def get_type(f, default='string'):
    try:
        return f.get_info()['type']
    except (KeyError, TypeError):
        return default

class Database(object):
    def on_start(self):
        self.last_value = None
        db_types = {'numeric': 'real',
                'string': 'text',
                'boolean': 'boolean'}
        try:
            type_str = db_types[self.get_info()['type']]
        except KeyError:
            type_str = db_types['string']

        self.db_name = self.module.module_name + '.db'
        db_conn = sqlite3.connect(self.db_name)

        # Create a new table for the field
        try:
            with db_conn:
                db_conn.execute(
                        'CREATE TABLE %s (time real primary key, value %s)'
                        % (self.field_name, type_str))
        except sqlite3.OperationalError as e:
            logging.exception(e)
            pass
        finally:
            db_conn.close()

    def _get_value(self):
        db_conn = sqlite3.connect(self.db_name)
        query = 'SELECT time, value FROM %s \
                ORDER BY time DESC LIMIT 1' \
                % (self.field_name,)
        try:
            c = db_conn.cursor()
            c.execute(query)
            re = c.fetchall()
            if re:
                return re[0]
        except Exception as e:
            logging.exception(e)
            return None
        finally:
            db_conn.close()
        return None

    def _get_value_at(self, t):
        db_conn = sqlite3.connect(self.db_name)
        query = 'SELECT time, value FROM %s \
                WHERE time < ? ORDER BY time DESC LIMIT 1' \
                % (self.field_name,)
        try:
            c = db_conn.cursor()
            c.execute(query, (t,))
            re = c.fetchall()
            if re:
                return re[0]
        except Exception as e:
            logging.exception(e)
            return None
        finally:
            db_conn.close()
        return None

    def _get_value_from_to(self, fr, to):
        db_conn = sqlite3.connect(self.db_name)
        query = 'SELECT time, value FROM %s \
                WHERE time < ?  AND time > ? ORDER BY time DESC' \
                % (self.field_name,)
        fr = int(fr)
        to = int(to)
        try:
            c = db_conn.cursor()
            c.execute(query, (to, fr))
            re = c.fetchall()
            return re
        except Exception as e:
            logging.exception(e)
            return []
        finally:
            db_conn.close()
        return []

    def set_value(self, t, value):
        db_conn = sqlite3.connect(self.db_name)
        query = 'INSERT INTO %s (time, value) VALUES (?, ?)' \
                % (self.field_name,)

        if get_type(self) == 'string':
            value = value.decode('utf-8')

        try:
            c = db_conn.cursor()
            c.execute(query, (t, value))
            db_conn.commit()
            self.last_value = (t, value)
            db_conn.close()
            return True
        except Exception as e:
            logging.exception(e)
            db_conn.rollback()
            db_conn.close()
            return False
        return False

class Volatile(object):
    volpersist_nb_values = 100
    volpersist_save_lost = True

    def __init__(self):
        super(Volatile, self).__init__()
        self._persisted_volatile_values = []

    def _get_value(self):
        if self._persisted_volatile_values:
            return sorted(self._persisted_volatile_values,
                    key = lambda x: x[0])[-1]
        return super(Volatile, self)._get_value()

    def _get_value_at(self, t):
        if self._persisted_volatile_values:
            v = sorted(self._persisted_volatile_values,
                    key = lambda x: abs(x[0] - t))[0]
            if abs(v[0] - t) <= type(self).update_rate:
                return v
        return super(Volatile, self)._get_value_at(t)

    def _get_value_from_to(self, fr, to):
        res = filter(lambda x: fr <= x[0] <= to,
                self._persisted_volatile_values)
        if res:
            return res
        return super(Volatile, self)._get_value_from_to(fr, to)

    def set_value(self, t, value):
        self._persisted_volatile_values += [(t, value)]
        if len(self._persisted_volatile_values) \
            > type(self).volpersist_nb_values:
                if type(self).volpersist_save_lost:
                    lost_value = self._persisted_volatile_values[0]
                    super(Volatile, self).set_value(*lost_value)
                self._persisted_volatile_values = \
                        self._persisted_volatile_values[1:]
        return True
