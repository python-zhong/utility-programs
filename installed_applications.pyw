from atexit import register as onexit
from collections import namedtuple
from os import getlogin
from tkinter import *
from tkinter.ttk import *
from tkinter.font import Font
from tkinter.scrolledtext import ScrolledText
from winreg import OpenKeyEx, HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE, EnumKey, EnumValue, KEY_READ
try:
    import ctypes; ctypes.oledll.shcore.SetProcessDpiAwareness(1)
except: pass
from sys import maxsize
IS_X64 = maxsize > 2 ** 32
Value = namedtuple('Value', ['name', 'value', 'type'])
def Enumerate(func, key):
    index = 0
    while True:
        try:
            yield func(key, index)
        except OSError:
            break
        index += 1
EnumerateKey = lambda key: [i for i in Enumerate(EnumKey, key)]
EnumerateValue = lambda key: [Value(*i) for i in Enumerate(EnumValue, key)]
with OpenKeyEx(HKEY_CURRENT_USER, 'Software', 0, KEY_READ) as _US:
    with OpenKeyEx(_US, 'Microsoft', 0, KEY_READ) as _UM:
        with OpenKeyEx(_UM, 'Windows', 0, KEY_READ) as _UW:
            with OpenKeyEx(_UW, 'CurrentVersion', 0, KEY_READ) as _UC:
                UU = OpenKeyEx(_UC, 'Uninstall', 0, KEY_READ)
    if IS_X64:
        with OpenKeyEx(_US, 'WOW6432Node') as _WOW64:
            with OpenKeyEx(_WOW64, 'Microsoft', 0, KEY_READ) as _UM:
                with OpenKeyEx(_UM, 'Windows', 0, KEY_READ) as _UW:
                    with OpenKeyEx(_UW, 'CurrentVersion', 0, KEY_READ) as _UC:
                        UUW64 = OpenKeyEx(_UC, 'Uninstall', 0, KEY_READ)
    else:
        UUW64 = None
with OpenKeyEx(HKEY_LOCAL_MACHINE, 'Software', 0, KEY_READ) as _LS:
    with OpenKeyEx(_LS, 'Microsoft', 0, KEY_READ) as _LM:
        with OpenKeyEx(_LM, 'Windows', 0, KEY_READ) as _LW:
            with OpenKeyEx(_LW, 'CurrentVersion', 0, KEY_READ) as _LC:
                LU = OpenKeyEx(_LC, 'Uninstall', 0, KEY_READ)
    if IS_X64:
        with OpenKeyEx(_LS, 'WOW6432Node') as _WOW64:
            with OpenKeyEx(_WOW64, 'Microsoft', 0, KEY_READ) as _LM:
                with OpenKeyEx(_LM, 'Windows', 0, KEY_READ) as _LW:
                    with OpenKeyEx(_LW, 'CurrentVersion', 0, KEY_READ) as _LC:
                        LUW64 = OpenKeyEx(_LC, 'Uninstall', 0, KEY_READ)
    else:
        LUW64=None
@onexit
def e():
    UU.Close()
    LU.Close()

def _WRAPPER(key):
    def _INNER(*, _key=key):
        installations = {}
        for k in Enumerate(EnumKey, _key):
            installations[k] = []
            with OpenKeyEx(_key, k, 0, KEY_READ) as key:
                for name, value, t in Enumerate(EnumValue, key):
                    installations[k].append(Value(name, value, t))
        return installations
    return _INNER
get_user_installations = _WRAPPER(UU)
get_local_installations = _WRAPPER(LU)
if IS_X64:
    get_user_installations_wow = _WRAPPER(UUW64)
    get_local_installations_wow = _WRAPPER(LUW64)
else:
    get_user_installations_wow = None
    get_local_installations_wow = None
tk = Tk(className='pkgmgr')
tk.title('Installed Packages')
style = Style()
style.configure('Treeview', rowheight=35)
tvf = Frame(tk)
tvf.pack(side=LEFT, fill=BOTH, expand=True)
tv = Treeview(tvf, show='tree', selectmode='browse')
tv.pack(side=LEFT, fill=BOTH, expand=True)
tfs = Scrollbar(tvf, command=tv.yview, orient=VERTICAL)
tfs.pack(side=RIGHT, fill=Y)
tv.config(yscrollcommand=tfs.set)

dtf = LabelFrame(tk, text='Detail')
dtf.pack(side=RIGHT, fill=BOTH, padx=2, pady=2, expand=True)
dt = ScrolledText(
    dtf,
    font=Font(family='Consolas', size=10),
    wrap='none',
    height=30,
    width=90
)
dt.pack(side=TOP, fill=BOTH, expand=True)
dts = Scrollbar(dtf, orient=HORIZONTAL, command=dt.xview)
dts.pack(side=BOTTOM, fill=X)
dt.config(xscrollcommand=dts.set)
tags = []
dt.insert('1.0', 'Choose One Item')
dt.tag_add('note', '1.0', END)
dt.tag_config('note', foreground='#AAAAAA')
tags.append('note')
dt.config(state=DISABLED)
ID_UI = tv.insert('', END, text='Installed For User `%s`' % getlogin(), tags='DEFAULT')
ID_LI = tv.insert('', END, text='Installed For All Users', tags='DEFAULT')
if IS_X64:
    ID_UI32 = tv.insert(ID_UI, index=END, text='x32', tags='DEFAULT')
    ID_UI64 = tv.insert(ID_UI, index=END, text='x64', tags='DEFAULT')
    ID_LI32 = tv.insert(ID_LI, index=END, text='x32', tags='DEFAULT')
    ID_LI64 = tv.insert(ID_LI, index=END, text='x64', tags='DEFAULT')
selections = {}
def update_sections():
    tv.selection_clear()
    if selections:
        tv.delete(*tuple(selections.keys()))
        selections.clear()
    if IS_X64:
        for k, v in get_user_installations().items():
            selections[tv.insert(ID_UI64, END, text=k)] = (k, v, 'User')
        for k, v in get_local_installations().items():
            selections[tv.insert(ID_LI64, END, text=k)] = (k, v, 'Local')
        for k, v in get_user_installations_wow().items():
            selections[tv.insert(ID_UI32, END, text=k)] = (k, v, 'User')
        for k, v in get_local_installations_wow().items():
            selections[tv.insert(ID_LI32, END, text=k)] = (k, v, 'Local')

    else:
        for k, v in get_user_installations().items():
            selections[tv.insert(ID_UI, END, text=k)] = (k, v, 'User')
        for k, v in get_local_installations().items():
            selections[tv.insert(ID_LI, END, text=k)] = (k, v, 'Local')
m = Menu()
tk.config(menu=m, padx=5, pady=5)
fm = Menu(tearoff=0)
m.add_cascade(label='File', menu=fm)
fm.add_command(label='Update', command=update_sections)
fm.add_separator()
fm.add_command(label='Exit', command=tk.destroy)
def onselect(_=None):
    selection = tv.selection()
    dt.config(state=NORMAL)
    if tags:
        dt.tag_delete(*tags)
        tags.clear()
    dt.delete('1.0', END)
    try:
        key, values, _ = selections[selection[0]]
    except LookupError:
        dt.insert('1.0', 'Choose One Item')
        dt.tag_add('note', '1.0', END)
        dt.tag_config('note', foreground='#AAAAAA')
        tags.append('note')
    else:
        keys = [str(i.name) for i in values] + ['ID']
        longest = 0
        for i in keys:
            if len(i) > longest:
                longest = len(i)
        text = f"{{:<{longest}}}: {{}}\n".format('ID', key)
        text += '\n'.join([f'{{:<{longest}}}: {{}}'.format(v.name, v.value if v.value is not None else '<Not Set>') for v in values])
        dt.insert('1.0', text.strip())
        i = 0
        ind = f'1.{longest}'
        dt.tag_add('index'+ind, f'1.0', ind)
        dt.tag_config('index'+ind, foreground='#10AAFF')
        tags.append('index'+ind)
        ind = f'1.{longest+2}'
        dt.tag_add('index'+ind, ind, f"1.end")
        tags.append('index'+ind)
        dt.tag_config('index'+ind, foreground='#AA70FF')    
        for i in range(1, len(values)+1):
            ind = f'{i+1}.{longest}'
            dt.tag_add('index'+ind, f'{i+1}.0', ind)
            dt.tag_config('index'+ind, foreground='#10AAFF')
            tags.append('index'+ind)
            v = values[i-1].value
            ind = f'{i+1}.{longest+2}'
            dt.tag_add('index'+ind, ind, f"{i+1}.end")
            tags.append('index'+ind)
            if isinstance(v, str):
                dt.tag_config('index'+ind, foreground='#801000')
            elif isinstance(v, int):
                dt.tag_config('index'+ind, foreground='#0020FF')
            elif isinstance(v, list):
                dt.tag_config('index'+ind, foreground='#00AA30')
            else:
                dt.tag_config('index'+ind, foreground='#808080')
    dt.config(state=DISABLED)
tv.bind('<<TreeviewSelect>>', onselect)
update_sections()
tk.mainloop()