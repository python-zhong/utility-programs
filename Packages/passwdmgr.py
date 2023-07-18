from base64 import b64encode, b64decode
import sqlite3
import os
from marshal import loads, dumps
encode = lambda pwd: b64encode(dumps(tuple(b64encode(pwd.encode(encoding='UTF-8'))))).decode(encoding='UTF-8')
decode = lambda data: b64decode(bytes(loads(b64decode(data.encode(encoding='UTF-8'))))).decode(encoding='UTF-8')
def new_database(path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.execute('CREATE TABLE maindb (name, value);')
    return conn
def _ensure_one(iterable, default=None):
    i = tuple(iterable)
    if len(i) < 1:
        return default
    else:
        return i[0]
insert_item = lambda cursor, item, data: cursor.execute("INSERT INTO maindb VALUES (?, ?);", (item, data))
remove_item = lambda cursor, item: cursor.execute("DELETE FROM maindb WHERE name=?;", (item, ))
list_items = lambda cursor: [i[0] for i in cursor.execute('SELECT name FROM maindb;')]
query_item = lambda cursor, item: _ensure_one(list(cursor.execute('SELECT value FROM maindb WHERE name=?;', (item, ))))
modify_item = lambda cursor, item, data: cursor.execute('UPDATE maindb SET name=?, value=? WHERE name=?', (item, data, item))
class DBMgr:
    def __init__(self, path):
        if not os.path.isfile(path):
            self.__conn = new_database(path)
        else:
            self.__conn = sqlite3.connect(path)
        self.__closed = False
    @property
    def items(self):
        return list_items(self.__conn.cursor())
    def query_item(self, item: str):
        n = query_item(self.__conn.cursor(), item)
        if n:
            return n[0]
    def remove_item(self, item):
        remove_item(self.__conn.cursor(), item)
    def insert_item(self, item, data):
        insert_item(self.__conn.cursor(), item, data)
    def modify_item(self, item, data):
        modify_item(self.__conn.cursor(), item, data)
    def close(self):
        self.__conn.commit()
        self.__conn.close()
        self.__closed = True
    @property
    def closed(self):
        return self.__closed
    def __getitem__(self, item):
        return self.query_item(item)
    def __setitem__(self, item, value):
        if item in self.items:
            self.modify_item(item, value)
        else:
            self.insert_item(item, value)
    def __delitem__(self, item):
        self.remove_item(item)
    def __enter__(self):
        return self
    def __exit__(self, *exc):
        self.close()
__all__ = ['encode', 'decode', 'show_passwd_safe', 'read_passwd', 'DBMgr']