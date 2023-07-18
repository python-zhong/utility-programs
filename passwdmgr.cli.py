from typing import Any
from Packages.passwdmgr import DBMgr, decode, encode
from Packages.consoleutil import choice_in_options, show_passwd_safe, read_passwd, input, putchars, putnewline, ASCII_FILTER, error, warn, info
import os
from sqlite3 import OperationalError
mgr = None
class _Sentiel:
    def __bool__(self):
        return False
    def __int__(self):
        return 0
    def __repr__(self):
        return '_Sentiel()'
    def __str__(self):
        return ''
    def __init_subclass__(cls):
        raise RuntimeError("'_Sentiel' is a final class")
    def __eq__(self, other):
        return isinstance(other, _Sentiel)
    def __hash__(self) -> int:
        return 0
    __slots__ = ()

_SENTIEL = _Sentiel()
OPTIONS = {
    'NOT_CONNECTED': (
        'Open / Create Password File',
        'Exit'
    ),
    'CONNECTED': (
        'Close Password File',
        'List Items',
        'Query Item',
        'Insert Item',
        'Modify Item',
        'Remove Item',
        'Exit'
    )
}
putchars('Password Manager (Version 0.0.1)', newline=True)
warn('WARNING: Current Version is under debug.')
def _h(c, ex, t=None, w=False):
    try:
        return c()
    except ex as e:
        if t:
            if w:
                error(t, *e.args)
            else:
                error(t)
        else:
            putnewline()
        return _SENTIEL
_O = "ERROR: Internal.Sqlite3.OperationalError: "
_E = "ERROR: Item not exists!"
_A = "ERROR: Item already exists!"
_N = "ERROR: No items!"
while True:
    try:
        if mgr is None:
            operation = choice_in_options(OPTIONS['NOT_CONNECTED'])
            if operation:
                break
            else:
                p = _h(lambda: input('File Path: ', min=1).strip(), KeyboardInterrupt)
                if p:
                    os.makedirs(os.path.dirname(p), exist_ok=True)
                    mgr = DBMgr(p)
        else:
            operation = choice_in_options(OPTIONS['CONNECTED'])
            if operation == 0:
                mgr.close()
                mgr = None
            elif operation == 1:
                items = _h(lambda: mgr.items, OperationalError, _O, w=True)
                if items is not None:
                    if not items:
                        info('No items.')
                        continue
                    info('Items:')
                    for i in items:
                        info('  ', i, important=False)
            elif operation == 2:
                items = _h(lambda: mgr.items, OperationalError, _O, w=True)
                if items != _SENTIEL:
                    if len(items) < 1:
                        error(_N)
                        continue    
                    item = _h(lambda: input('Item Name: ', filter=ASCII_FILTER, min=1).strip(), KeyboardInterrupt)
                    if item != _SENTIEL:
                        if item not in items:
                            error(_E)
                            continue
                        query = _h(lambda: mgr.query_item(item), OperationalError, _O, w=True)
                        if query != _SENTIEL:
                            if not query:
                                info('Password is empty.')
                            else:
                             show_passwd_safe(decode(query))
            elif operation == 3:
                item = _h(lambda: input('New Item Name: ', filter=ASCII_FILTER, min=1).strip(), KeyboardInterrupt)
                if item != _SENTIEL:
                    if item in mgr.items:
                        error(_A)
                    else:
                        pwd = _h(lambda: read_passwd(), KeyboardInterrupt)
                        if pwd != _SENTIEL:    
                            _h(lambda: mgr.insert_item(item, encode(pwd)), OperationalError, _O, w=True)
            elif operation == 4:
                items = _h(lambda: mgr.items, OperationalError, _O, w=True)
                if items != _SENTIEL:
                    if len(items) < 1:
                        error(_N)
                        continue
                    item = _h(lambda: input('Item Name: ', filter=ASCII_FILTER, min=1).strip(), KeyboardInterrupt)
                    if item != _SENTIEL:
                        if item not in items:
                            error(_N)
                        else:
                            
                            pwd = _h(lambda: read_passwd('New Password: '), KeyboardInterrupt)
                            if pwd != _SENTIEL:
                                _h(lambda: mgr.modify_item(item, encode(pwd)), OperationalError, _O, w=True)
            elif operation == 5:
                items = _h(lambda: mgr.items, OperationalError, _O, w=True)
                if items != _SENTIEL:
                    if len(items) < 1:
                        error(_N)
                        continue
                    item = _h(lambda: input('Item Name: ', filter=ASCII_FILTER, min=1).strip(), KeyboardInterrupt)
                    if item != _SENTIEL:
                        if item not in items:
                            error('ERROR: Item not exist!')
                        else:
                            _h(lambda: mgr.remove_item(item), OperationalError, _O, w=True)
            elif operation == 6:
                mgr.close()
                break
    except KeyboardInterrupt:
        if mgr:
            mgr.close()
        break
