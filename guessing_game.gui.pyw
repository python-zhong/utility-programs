from random import SystemRandom
from tkinter import *
from tkinter.ttk import *
from tkinter import Label
from tkinter.font import Font
from tkinter.messagebox import showerror, showinfo
try: import ctypes; ctypes.oledll.shcore.SetProcessDpiAwareness(1)
except: pass
random = SystemRandom()
maximum = random.randint(1, 100) * 100
secret = random.randint(0, maximum)
tk = Tk(className="guessing_game")
tk.resizable(False, False)
tk.config(padx=5, pady=5)
rounds = IntVar(tk, 1)
tk.title("Guessing Game")
default_font = Font(family="Consolas", size=12)
range_f = Frame(tk)
range_f.pack(side=TOP)
Label(range_f, text="[ Round", fg="#640000").pack(side=LEFT)
Label(range_f, textvariable=rounds, fg="green", font=default_font).pack(side=LEFT)
Label(range_f, text="]", fg='#640000').pack(side=LEFT)
Label(range_f, text="Guess a number from").pack(side=LEFT)
Label(range_f, text="0", fg="blue", font=default_font).pack(side=LEFT)
Label(range_f, text="to").pack(side=LEFT)
Label(range_f, text=str(maximum), fg="blue", font=default_font).pack(side=LEFT)
hslf = LabelFrame(tk, text="History")
hslf.pack(side=TOP, fill=BOTH, expand=True)
hs = Listbox(hslf)
hs.pack(side=LEFT, fill=BOTH, expand=True)
sb = Scrollbar(hslf, orient=VERTICAL, command=hs.yview)
sb.pack(side=RIGHT, fill=Y)
hs.config(yscrollcommand=sb.set)
cframe = Frame(tk)
cframe.pack(side=TOP, fill=X)
num = Entry(cframe, width=len(str(maximum)), font=default_font)
num.pack(side=LEFT, fill=BOTH)
num.focus()
def guess(_=None):
    n = num.get().strip()
    if not n.isdigit():
        showerror('Error', 'Please input a number!')
        return
    try:
        n = int(n)
    except:
        showerror("Error", "Please input a number!")
        return
    if n == secret:
        showinfo("Info", "You Win!\nYou uses %d rounds." % rounds.get())
        tk.destroy()
        return
    elif n > secret:
        showinfo("Info", "The number is bigger!")
        hs.insert(END, '[Round %d] %d > secret number' % (rounds.get(), n))
    elif n < secret:
        showinfo("Info", "The number is smaller!")
        hs.insert(END, '[Round %d] %d < secret number' % (rounds.get(), n))
    rounds.set(rounds.get()+1)
    num.focus()
    num.delete(0, END)
num.bind('<Return>', guess)
def onExit(_=None):
    showinfo("Info", "Ok, the secret number is %d" % secret)
    tk.destroy()
tk.bind("<Alt-F4>", onExit)
Button(cframe, text="Guess", command=guess).pack(side=LEFT)
Button(cframe, text="Exit", command=onExit).pack(side=RIGHT)
tk.mainloop()