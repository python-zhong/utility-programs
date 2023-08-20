from random import SystemRandom
from tkinter import *
from tkinter.ttk import *
from tkinter.font import Font
from tkinter.messagebox import showerror, showinfo
from time import time_ns, sleep
from threading import Thread
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
default_font = Font(family="Consolas", size=10)
input_font = Font(family="Consolas", size=12)
range_f = Frame(tk)
range_f.pack(side=TOP)
style = Style()
style.configure("M.TLabel", foreground="#640000")
style.configure("G.TLabel", foreground="green")
style.configure("B.TLabel", foreground="blue")
style.configure("T.TLabel", foreground="teal")
Label(range_f, text="[ Round", style="M.TLabel", font=default_font).pack(side=LEFT)
Label(range_f, textvariable=rounds, style="G.TLabel", font=default_font).pack(side=LEFT, padx=5)
Label(range_f, text="]", style="M.TLabel", font=default_font).pack(side=LEFT)
Label(range_f, text="Guess a number from", font=default_font).pack(side=LEFT, padx=5)
Label(range_f, text="0", style="B.TLabel", font=default_font).pack(side=LEFT)
Label(range_f, text="to", font=default_font).pack(side=LEFT, padx=5)
Label(range_f, text=str(maximum), style="B.TLabel", font=default_font).pack(side=LEFT)
hslf = LabelFrame(tk, text="History")
hslf.pack(side=TOP, fill=BOTH, expand=True)
hs = Listbox(hslf, exportselection=False, activestyle=NONE, font=default_font)
hs.pack(side=LEFT, fill=BOTH, expand=True)
sb = Scrollbar(hslf, orient=VERTICAL, command=hs.yview)
sb.pack(side=RIGHT, fill=Y)
hs.config(yscrollcommand=sb.set)
cframe = Frame(tk)
cframe.pack(side=TOP, fill=X)
tm = Label(cframe, text="0:00:00:000", font=default_font, style="T.TLabel")
tm.pack(side=LEFT)
num = Entry(cframe, width=len(str(maximum))+1, font=input_font, foreground="green", justify=CENTER)
num.pack(side=LEFT, fill=BOTH)
num.focus()
def split_milliseconds(milliseconds):
    seconds = milliseconds // 1000
    milliseconds %= 1000
    minutes = seconds // 60
    seconds %= 60
    hours = minutes // 60
    minutes %= 60
    return hours, minutes, seconds, milliseconds
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
        end_time_ns = time_ns() // 1000 // 1000
        due = end_time_ns - start_time_ms
        times = "%dh %dm %ds %dms" % split_milliseconds(due)
        showinfo("Info", "You Win!\nYou uses %d rounds and %s." % (rounds.get(), times))
        tk.destroy()
        return
    elif n > secret:
        showinfo("Info", "The number is bigger!")
        hs.insert(END, 'Round %-3d: %6d > secret number' % (rounds.get(), n))
    elif n < secret:
        showinfo("Info", "The number is smaller!")
        hs.insert(END, 'Round %-3d: %6d < secret number' % (rounds.get(), n))
    rounds.set(rounds.get()+1)
    num.focus()
    num.delete(0, END)
num.bind('<Return>', guess)
def onExit(_=None):
    showinfo("Info", "Ok, the secret number is %d" % secret)
    tk.destroy()
tk.bind("<Alt-F4>", onExit)
tk.protocol("WM_DELETE_WINDOW", onExit)
Button(cframe, text="Guess", command=guess).pack(side=LEFT)
Button(cframe, text="Exit", command=onExit).pack(side=RIGHT)
start_time_ms = time_ns() // 1000 // 1000
def update_conter():
    sleep(0.01)
    while True:
        current_time_ms = time_ns() // 1000 // 1000
        h, m, s, ms = split_milliseconds(current_time_ms-start_time_ms)
        if m < 10: m = "0%d"%m
        if s < 10: s = "0%d"%s
        if ms < 10: ms = "00%d"%ms
        elif ms < 100: ms = "0%d"%ms
        try:
            tk.update()
            tm.config(text="%s:%s:%s:%s"%(h, m, s, ms))
        except:
            break
td = Thread(target=update_conter)
td.start()
sleep(0.01)
tk.mainloop()
td.join()