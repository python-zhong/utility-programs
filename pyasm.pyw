from idlelib.colorizer import ColorDelegator
from idlelib.percolator import Percolator
from idlelib.textview import view_text
from idlelib.config import idleConf
from tkinter import *
from tkinter.font import Font
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import *
from traceback import format_exception
try:
    from winsound import PlaySound, SND_ALIAS, SND_ASYNC
    ErrorSound = lambda: PlaySound('SystemHand', flags=SND_ALIAS | SND_ASYNC)
except:
    ErrorSound = lambda: None
import sys
import dis
import types
from uuid import uuid1
banner     = "======================= Assembly Start ======================="
banner_end = "======================= Assembly Ended ======================="
COLOR_POOL = {
    "String" : "#640000",
    "Integer": "#006040",
    "Lineno" : "gray",
    "Offset" : "indigo",
    "Mark"   : "orange",
    "Comment": "gray",
    "Unknown": "teal",
    "Command": "blue",
    "Item"   : "#0080EE"
}
def write_code_info(co: "types.CodeType"):
    write_line("Name", COLOR_POOL["Item"], False)
    write_line("                     : ", newline=False)
    write_line(co.co_name, COLOR_POOL["String"])
    write_line("Filename", COLOR_POOL["Item"], False)
    write_line("                 : ", newline=False)
    write_line(co.co_filename, COLOR_POOL["String"])
    write_line("Argument Count", COLOR_POOL["Item"], False)
    write_line("           : ", newline=False)
    write_line(co.co_argcount, COLOR_POOL["Integer"])
    write_line("Positional-Only Arguments", COLOR_POOL["Item"], False)
    write_line(": ", newline=False)
    write_line(co.co_posonlyargcount, COLOR_POOL["Integer"])
    write_line("Keyword-Only Arguments", COLOR_POOL["Item"], False)
    write_line("   : ", newline=False)
    write_line(co.co_kwonlyargcount, COLOR_POOL["Integer"])
    write_line("Number of locals", COLOR_POOL["Item"], False)
    write_line("         : ", newline=False)
    write_line(co.co_nlocals, COLOR_POOL["Integer"])
    write_line("Stack Size", COLOR_POOL["Item"], False)
    write_line("               : ", newline=False)
    write_line(co.co_stacksize, COLOR_POOL["Integer"])
    write_line("Flags", COLOR_POOL["Item"], False)
    write_line("                    : ", newline=False)
    write_line(dis.pretty_flags(co.co_flags).replace(',', ' |'), COLOR_POOL["Offset"])
    if co.co_consts:
        write_line("Constants", COLOR_POOL["Item"], False)
        write_line(":")
        for i, n in enumerate(co.co_consts):
            write_line("%6d" % i, COLOR_POOL["Lineno"], newline=False)
            write_line(": ", newline=False)
            write_line(repr(n), COLOR_POOL["Unknown"])
    if co.co_names:
        write_line("Names", COLOR_POOL["Item"], False)
        write_line(":")
        for i, n in enumerate(co.co_names):
            write_line("%6d" % i, COLOR_POOL["Lineno"], newline=False)
            write_line(": ", newline=False)
            write_line(repr(n), COLOR_POOL["Unknown"])
    if co.co_varnames:
        write_line("Variable Names", COLOR_POOL["Item"], False)
        write_line(":")
        for i, n in enumerate(co.co_names):
            write_line("%6d" % i, COLOR_POOL["Lineno"], newline=False)
            write_line(": ", newline=False)
            write_line(repr(n), COLOR_POOL["Unknown"])
    if co.co_freevars:
        write_line("Free Variables", COLOR_POOL["Item"], False)
        write_line(":")
        for i, n in enumerate(co.co_freevars):
            write_line("%6d" % i, COLOR_POOL["Lineno"], newline=False)
            write_line(": ", newline=False)
            write_line(repr(n), COLOR_POOL["Unknown"])
    if co.co_cellvars:
        write_line("Cell Variables", COLOR_POOL["Item"], False)
        write_line(":")
        for i, n in enumerate(co.co_names):
            write_line("%6d" % i, COLOR_POOL["Lineno"], newline=False)
            write_line(": ", newline=False)
            write_line(repr(n), COLOR_POOL["Unknown"])
def write_assembly(co: "types.CodeType"):
    write_line("Assembly of ", COLOR_POOL["Comment"], False)
    write_line(repr(co), COLOR_POOL["Unknown"], False)
    write_line(':')
    write_code_info(co)
    write_line(banner, COLOR_POOL["Comment"])
    linestarts = dict(dis.findlinestarts(co))
    line_offset = 0
    exception_entries = dis._parse_exception_table(co)
    instructions: list[dis.Instruction] = list(dis._get_instructions_bytes(
        dis._get_code_array(co, use_adaptive.get()),
        co._varname_from_oparg,
        co.co_names, co.co_consts,
        linestarts, line_offset,
        exception_entries,
        co.co_positions(),
        show_cache.get()
    ))
    max_startsline = 10
    max_offset = 6
    max_opcode = 14
    max_opname = 14
    max_arguments = 0
    for i in instructions:
        if i.starts_line is not None:
            max_startsline = max(max_startsline, len(str(i.starts_line)))
        max_offset = max(max_offset, len(str(i.offset)))
        max_opcode = max(max_opcode, len(str(i.opcode)))
        max_opname = max(max_opname, len(str(i.opname)))
        if i.arg:
            max_arguments = max(max_arguments, len(str(i.arg)))
    COLUMN_HEAD = (
        f"{'Start Line'.ljust(max_startsline)}|{'Offset'.ljust(max_offset)}|Mark|"
        f"{'Operation Code'.ljust(max_opcode)}|{'Operation Name'.ljust(max_opname)}|Arguments"
    )
    write_line(COLUMN_HEAD, COLOR_POOL['Comment'])
    for i in instructions:
        if i.starts_line is None:
            write_line(''.ljust(max_startsline+1), newline=False)
        else:
            write_line(f'{i.starts_line}'.ljust(max_startsline+1), COLOR_POOL["Lineno"], False)
        write_line(f'{i.offset}'.ljust(max_offset+1), COLOR_POOL["Offset"], False)
        if i.is_jump_target:
            write_line(" >>  ", COLOR_POOL["Mark"], False)
        else:
            write_line("     ", newline=False)
        write_line(f"{i.opcode}".ljust(max_opcode+1), COLOR_POOL['Integer'], False)
        write_line(i.opname.ljust(max_opname+1), COLOR_POOL["Command"], False)
        if i.arg is None:
            write_line("")
        else:
            write_line(f"{i.arg}".ljust(max_arguments), COLOR_POOL["Integer"], False)
            if i.argrepr:
                write_line(f" ({i.argrepr})", COLOR_POOL["Comment"])
            else:
                write_line("")
    if exception_entries:
        write_line("Exception Table", COLOR_POOL["Item"], False)
        write_line(':')
        max_start = max_end = max_target = 0
        for entry in exception_entries:
            end = entry.end-2
            if len(str(entry.start)) > max_start:
                max_start = len(str(entry.start))
            if len(str(end)) > max_end:
                max_end = len(str(end))
            if len(str(entry.target)) > max_target:
                max_target = len(str(entry.target))
        for entry in exception_entries:
            end = entry.end-2
            write_line("  ", newline=False)
            write_line(str(entry.start).ljust(max_start), COLOR_POOL["Offset"], False)
            write_line(" to ", COLOR_POOL["Comment"], False)
            write_line(str(end).ljust(max_end), COLOR_POOL["Offset"], False)
            write_line(" -> ", COLOR_POOL["Mark"], False)
            write_line(str(entry.target).ljust(max_target), COLOR_POOL["Offset"], False)
            write_line(" [", COLOR_POOL["Unknown"], False)
            write_line(entry.depth, COLOR_POOL["Integer"], False)
            write_line("]", COLOR_POOL["Unknown"], False)
            if entry.lasti:
                write_line(" ", newline=False)
                write_line("(lasti)", COLOR_POOL["Comment"])
            else:
                write_line("")
    write_line(banner_end, COLOR_POOL["Comment"])
    for x in co.co_consts:
        if hasattr(x, "co_code"):
            write_assembly(x)
tk = Tk()
tk.title("Python Assembler")
tk.resizable(False, False)
tk.config(padx=10, pady=10)
font = idleConf.GetFont(tk, 'main', 'EditorWindow')
font = Font(family=font[0], size=10, weight=font[2])
fm = Frame()
fm.pack(side=TOP, fill=BOTH, padx=5, pady=5)
lf1 = LabelFrame(fm, text='Python Code')
lf1.pack(side=LEFT, fill=BOTH)
text = ScrolledText(lf1, font=font, wrap=NONE)
text.pack(side=TOP, fill=BOTH)
sb1 = Scrollbar(lf1, orient=HORIZONTAL, command=text.xview)
sb1.pack(side=BOTTOM, fill=BOTH)
text.config(xscrollcommand=sb1.set)
lf2 = LabelFrame(fm, text='Assembly Output')
lf2.pack(side=RIGHT, fill=BOTH)
res = ScrolledText(lf2, font=font, state='disabled', wrap=NONE)
res.pack(side=TOP, fill=BOTH)
sb2 = Scrollbar(lf2, orient=HORIZONTAL, command=res.xview)
sb2.pack(side=BOTTOM, fill=BOTH)
res.config(xscrollcommand=sb2.set)
Percolator(text).insertfilter(ColorDelegator())
tag_table = []
current_line = 1
current_char = 0
show_cache = BooleanVar(tk, True)
use_adaptive = BooleanVar(tk, False)
def write_line(text, color=None, newline=True):
    text = str(text)
    global current_line, current_char
    if newline:
        text += '\n'
    res.insert(END, text)
    if color:
        tg = str(uuid1())
        res.tag_add(tg, f'{current_line}.{current_char}', f"{current_line}.end")
        res.tag_config(tg, foreground=color, selectforeground='white')
        tag_table.append(tg)
    if newline:
        current_char = 0
        current_line += 1
    else:
        current_char += len(text)
def compile_dis():
    t = text.get('1.0', END)
    try:
        ct = compile(source=t, filename='<string>', mode='eval')
    except:
        ct = None
    if ct is None:
        try:
            ct = compile(source=t, filename='<string>', mode='exec')
        except:
            exc, value, tb = sys.exc_info()
            tb = tb.tb_next
            ErrorSound()
            view_text(tk, 'Compile Error', ''.join(format_exception(exc, value, tb)), wrap=NONE)
            return
    clear_assembly()
    res.config(state=NORMAL)
    write_assembly(ct)
    res.config(state=DISABLED)
def clear_assembly():
    global current_line, current_char
    current_line = 1
    current_char = 0
    res.config(state=NORMAL)
    if tag_table:
        res.tag_delete(*tag_table)
        tag_table.clear()
    res.delete('1.0', END)
    res.config(state=DISABLED)
bfm = Frame(tk)
bfm.pack(side=BOTTOM, fill=Y)
Button(bfm, command=tk.destroy, text='Exit').grid(column=0, row=0)
Button(bfm, command=compile_dis, text='Assembly').grid(column=1, row=0)
Button(bfm, command=clear_assembly, text='Clear Assembly Output').grid(column=2, row=0)
Checkbutton(bfm, variable=show_cache, text="Show Cache").grid(column=3, row=0)
Checkbutton(bfm, variable=use_adaptive, text="Use Adaptive Code").grid(column=4, row=0)
tk.mainloop()