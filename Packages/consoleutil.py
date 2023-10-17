from msvcrt import getwch, putwch
import builtins
from .ansiutil import *
GENERIC_FILTER = lambda n: True
ASCII_FILTER = lambda n: 0x20 <= ord(n) < 0x7F
NUMBER_FILTER = lambda n: 0x30 <= ord(n) <= 0x39
__CHOICE_FILTER_BUILDER = lambda *choices: lambda n: n in choices

def putchars(*values, for_color=False, sep='', newline=False):
    sep = str(sep)
    if for_color:
        return builtins.print(*values, sep=sep, end='\n' if newline else '', flush=True)
    values = map(str, values)
    for chars in values:
        for index, char in enumerate(chars):
            putwch(char)
            if index < len(chars) - 1 and sep:
                for s in sep:
                    putwch(s)
    if newline:
        putwch('\r')
        putwch('\n')
_m = lambda *msg, fg, important: putchars(format_text(''.join(map(str, msg)), fg=fg, bold=important), for_color=True, newline=True)
error = lambda *msg, important=True: _m(*msg, fg='red', important=important)
info = lambda *msg, important=True: _m(*msg, fg='bright_white', important=important)
warn = lambda *msg, important=True: _m(*msg, fg='yellow', important=important)
def show_passwd_safe(pwd, tip='Password (Use "←" key and "→" key to scroll, ESC to finish): '):
    putchars(tip + ('*'*len(pwd)))
    for _ in range(len(pwd)):
        putbackspace()
    index = 0
    putwch(pwd[0])
    while True:
        n = getwch()
        if n == '\003' or n == '\x1b':
            while index >= 0:
                putbackspace()
                index -= 1
            for _ in range(len(pwd)):
                putwch('*')
            putnewline()
            return
        elif n == '\xe0':
            n = getwch()
            if n == 'K':
                if index > 0:
                    putbackspace()
                    putwch('*')
                    putbackspace(2)
                    index -= 1
                    putwch(pwd[index])
            elif n == 'M':
                if index < len(pwd) - 1:
                    putbackspace()
                    putwch('*')
                    index += 1
                    putwch(pwd[index])
            elif n == 'G':
                while index > 0:
                    putbackspace()
                    putwch('*')
                    putbackspace(2)
                    index -= 1
                    putwch(pwd[index])
            elif n == 'O':
                while index < len(pwd) - 1:
                    putbackspace()
                    putwch('*')
                    index += 1
                    putwch(pwd[index])
def getchars(echo=None, filter=None, min=None, max=None):
    if echo is None and filter in (None, GENERIC_FILTER):
        return builtins.input()
    if min is not None:
        if not isinstance(min, int):
            raise TypeError("`min` can only be possitive integers")
        elif min < 0:
            raise ValueError("`min` can only be possitive integers")
    else:
        min = 0
    if max is not None:
        if not isinstance(max, int):
            raise TypeError("`max` can only be possitive integers that greater or equal `min`.")
        elif max < min:
            raise ValueError("`max` can only be possitive integers that greater or equal `min`.")
    if echo is not None:
        if not isinstance(echo, str):
            raise TypeError("`echo` can only be a char, not others!")
        elif len(echo) > 1:
            raise ValueError("`echo` is a char!")
    data = ''
    current_index = 0
    while True:
        n = getwch()
        if n == '\n' or n == '\r' and len(data) >= min:
            putnewline()
            break
        elif n == '\003':
            putchars('^C')
            raise KeyboardInterrupt
        elif n == '\004':
            putchars('^D')
            raise EOFError
        elif n == '\032':
            putchars('^Z')
            raise EOFError
        elif n == '\b':
            if data and current_index > 0:
                data = data[:current_index-1] + data[current_index:]
                current_index -= 1
                if echo != '':
                    erase_back_chars()
                    puts = data[current_index:] + ' '
                    if echo and len(puts) > 1:
                        puts = echo * (len(puts)-1) + ' '
                    putchars(puts)
                    putbackspace(len(puts))
        elif n == '\xe0':
            if echo != '':
                next = getwch()
                if next == 'K': # "←" Pressed
                    if current_index > 0:
                        current_index -= 1
                        putbackspace()
                elif next == 'M': # "→" Pressed
                    if current_index < len(data):
                        putwch(data[current_index] if echo is None else echo)
                        current_index += 1
                elif next == 'G': # "Home" Pressed
                    if current_index > 0:
                        putbackspace(current_index)
                        current_index = 0
                elif next == 'O': # "End" Pressed
                    puts = data[current_index:]
                    if echo:
                        puts = echo * len(puts)
                    putchars(puts)
                    current_index = len(data)
        elif filter(n):
            if max:
                if len(data) >= max:
                    continue
            data = data[:current_index] + n + data[current_index:]
            if echo != '':
                current_index += 1
                putwch(n if echo is None else echo)
                puts = data[current_index:]
                if echo:
                    puts = echo * len(puts)
                for i in puts:
                    putwch(i)
                putbackspace(len(puts))
    return data
def input(prompt='', echo=None, filter=None, min=None, max=None):
    putchars(format_text(prompt, fg='bright_white'))
    return getchars(echo, filter, min=min, max=max)
def read_passwd(tip="Password: "):
    return input(tip, echo='*', filter=ASCII_FILTER, min=1)
def choice_in_options(options, tip="Choose an operation:"):
    if len(options) < 1:
        raise ValueError
    info(tip)
    while True:
        for index, item in enumerate(options):
            putchars('  [', format_text(index, fg="bright_white", bold=True, underline=True),']: ', format_text(item, fg='bright_white'), for_color=True, newline=True)
        num = input('> ', filter=__CHOICE_FILTER_BUILDER(*tuple(map(str, range(len(options))))), min=1, max=len(str(len(options))))
        num = int(num)
        if 0 <= num < len(options):
            return num
        error('ERROR: Please choose one of these items!')