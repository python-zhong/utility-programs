import Packages.winerrquery as winerrquery
from tkinter import *
from tkinter.ttk import *
from tkinter.font import Font
from tkinter.messagebox import showerror, showwarning
try:
    from ctypes import oledll
    oledll.LoadLibrary('shcore').SetProcessDpiAwareness(1)
except:
    pass
tk = Tk(className='errlook')
tk.resizable(False, False)
font = Font(family='Consolas', size=10)
tk.title('Error Look')
ef = Frame(tk)
ef.pack(side=TOP, fill=X)
result = Text(tk, font=font, background='#F4F4F4', state=DISABLED, width=45, height=15)
result.pack(side=BOTTOM, fill=BOTH, expand=True)
Label(ef, text='Errno:').pack(side=LEFT)
code = Entry(ef, width=10, font=font)
code.pack(side=LEFT)
def f(_=None):
    c = code.get().lower().strip()
    try:
        if 'x' in c:
            num = int(c, base=16)
        elif 'b' in c:
            num = int(c, base=2)
        elif c.startswith("0o"):
            num = int(c, base=8)
        elif c.startswith("0") and len(c) > 1:
            num = int(c, base=8)
        else:
            num = int(c)
    except:
        showerror('Error', f'"{c}" is not a number')
        return
    if not 0 <= num <= 0xFFFFFFFF:
        showerror('Error', f'Errno must between 0 and 0xFFFFFFFF')
        return
    r = winerrquery.query(num)
    if r:
        result.config(state=NORMAL)
        result.delete(1.0, END)
        result.insert(1.0, r)
        result.config(state=DISABLED)
    else:
        showwarning('Message', f'Errno [{c}] not found')
query = Button(ef, text='Find', command=f)
query.pack(side=LEFT)
code.bind('<Return>', f)
Button(ef, text='Exit', command=tk.destroy).pack(side=RIGHT)
tk.mainloop()