from winreg import OpenKeyEx, HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE, EnumKey, EnumValue, KEY_READ
import atexit
from collections import namedtuple
from tkinter import *
from tkinter.ttk import *
from tkinter.font import Font
from tkinter.scrolledtext import ScrolledText
from os import getlogin
try:
    import ctypes; ctypes.oledll.shcore.SetProcessDpiAwareness(1)
except: pass
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
with OpenKeyEx(HKEY_LOCAL_MACHINE, 'Software', 0, KEY_READ) as _LS:
    with OpenKeyEx(_LS, 'Microsoft', 0, KEY_READ) as _LM:
        with OpenKeyEx(_LM, 'Windows', 0, KEY_READ) as _LW:
            with OpenKeyEx(_LW, 'CurrentVersion', 0, KEY_READ) as _LC:
                LU = OpenKeyEx(_LC, 'Uninstall', 0, KEY_READ)
@atexit.register
def onexit():
    UU.Close()
    LU.Close()

def get_user_installations():
    installations = {}
    for k in Enumerate(EnumKey, UU):
        installations[k] = []
        with OpenKeyEx(UU, k, 0, KEY_READ) as key:
            for name, value, t in Enumerate(EnumValue, key):
                installations[k].append(Value(name, value, t))
    return installations
def get_local_installations():
    installations = {}
    for k in Enumerate(EnumKey, LU):
        installations[k] = []
        with OpenKeyEx(LU, k, 0, KEY_READ) as key:
            for name, value, t in Enumerate(EnumValue, key):
                installations[k].append(Value(name, value, t))
    return installations

tk = Tk(className='pkgmgr')
tk.title('Installed Packages')
tk.resizable(False, False)
style = Style()
style.configure('Treeview', rowheight=30)
tvf = Frame(tk)
tvf.pack(side=LEFT)
tv = Treeview(tvf, show='tree', selectmode='browse', height=28)
tv.pack(side=LEFT, fill=BOTH)
tfs = Scrollbar(tvf, command=tv.yview, orient=VERTICAL)
tfs.pack(side=RIGHT, fill=Y)
tv.config(yscrollcommand=tfs.set)
dtf = LabelFrame(tk, text='Detail')
dtf.pack(side=RIGHT, fill=BOTH, padx=5, pady=5)
dt = ScrolledText(
    dtf,
    font=Font(family='Consolas', size=10),
    wrap='none',
    height=35,
    width=120
)
dt.pack(side=TOP, fill=BOTH, padx=5)
dts = Scrollbar(dtf, orient=HORIZONTAL, command=dt.xview)
dts.pack(side=BOTTOM, fill=X)
dt.config(xscrollcommand=dts.set)
tags = []
dt.insert('1.0', 'Choose One Item')
dt.tag_add('note', '1.0', END)
dt.tag_config('note', foreground='#AAAA00')
tags.append('note')
dt.config(state=DISABLED)
ID_UI = tv.insert('', END, text='Installed For User `%s`' % getlogin(), tags='DEFAULT')
ID_LI = tv.insert('', END, text='Installed For All Users', tags='DEFAULT')
selections = {}
def update_sections():
    tv.selection_clear()
    if selections:
        tv.delete(*tuple(selections.keys()))
        selections.clear()
    for k, v in get_user_installations().items():
        selections[tv.insert(ID_UI, END, text=k)] = (k, v, 'User')
    for k, v in get_local_installations().items():
        selections[tv.insert(ID_LI, END, text=k)] = (k, v, 'Local')
m = Menu()
tk.config(menu=m, padx=10, pady=10)
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
    if not selection or ID_LI in selection or ID_UI in selection:
        dt.insert('1.0', 'Choose One Item')
        dt.tag_add('note', '1.0', END)
        dt.tag_config('note', foreground='#AAAA00')
        tags.append('note')
    else:
        key, values, _ = selections[selection[0]]
        keys = [str(i.name) for i in values] + ['UUID/Name']
        longest = 0
        for i in keys:
            if len(i) > longest:
                longest = len(i)
        text = f"{{:<{longest}}}: {{}}\n".format('UUID/Name', key)
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