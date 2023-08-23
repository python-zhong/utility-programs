from msvcrt import getwch, putwch
from .win32confix import fix_windows_console
import builtins
fix_windows_console()
GENERIC_FILTER = lambda n: True
ASCII_FILTER = lambda n: 0x20 <= ord(n) < 0x7F
NUMBER_FILTER = lambda n: 0x30 <= ord(n) <= 0x39
__CHOICE_FILTER_BUILDER = lambda *choices: lambda n: n in choices
def style_output(
        text,
        fg=None, bg=None,
        bold=None, dim=None, underline=None, overline=None, italic=None,
        blink=None,reverse=None, strikethrough=None, reset=True
    ):
    _ansi_colors = {
        "black": 30,
        "red": 31,
        "green": 32,
        "yellow": 33,
        "blue": 34,
        "magenta": 35,
        "cyan": 36,
        "white": 37,
        "reset": 39,
        "bright_black": 90,
        "bright_red": 91,
        "bright_green": 92,
        "bright_yellow": 93,
        "bright_blue": 94,
        "bright_magenta": 95,
        "bright_cyan": 96,
        "bright_white": 97,
    }
    _ansi_reset_all = "\033[0m"
    def _interpret_color(color, offset=0) -> str:
        if isinstance(color, int):
            return f"{38 + offset};5;{color:d}"

        if isinstance(color, (tuple, list)):
            r, g, b = color
            return f"{38 + offset};2;{r:d};{g:d};{b:d}"
        return str(_ansi_colors[color] + offset)
    if not isinstance(text, str):
        text = str(text)
    bits = []
    if fg:
        try:
            bits.append(f"\033[{_interpret_color(fg)}m")
        except KeyError:
            raise TypeError(f"Unknown color {fg!r}") from None
    if bg:
        try:
            bits.append(f"\033[{_interpret_color(bg, 10)}m")
        except KeyError:
            raise TypeError(f"Unknown color {bg!r}") from None
    if bold is not None:
        bits.append(f"\033[{1 if bold else 22}m")
    if dim is not None:
        bits.append(f"\033[{2 if dim else 22}m")
    if underline is not None:
        bits.append(f"\033[{4 if underline else 24}m")
    if overline is not None:
        bits.append(f"\033[{53 if overline else 55}m")
    if italic is not None:
        bits.append(f"\033[{3 if italic else 23}m")
    if blink is not None:
        bits.append(f"\033[{5 if blink else 25}m")
    if reverse is not None:
        bits.append(f"\033[{7 if reverse else 27}m")
    if strikethrough is not None:
        bits.append(f"\033[{9 if strikethrough else 29}m")
    bits.append(text)
    if reset:
        bits.append(_ansi_reset_all)
    return "".join(bits)
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
def putbackspace(n=1):
    putchars('\b'*n)
def erase_back_chars(n=1):
    putchars('\b \b'*n)
def putnewline(n=1):
    for _ in range(n):
        putchars(newline=True)
_m = lambda *msg, fg, important: putchars(style_output(''.join(map(str, msg)), fg=fg, bold=important), for_color=True, newline=True)
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
    putchars(style_output(prompt, fg='bright_white'))
    return getchars(echo, filter, min=min, max=max)
def read_passwd(tip="Password: "):
    return input(tip, echo='*', filter=ASCII_FILTER, min=1)
def choice_in_options(options, tip="Choose an operation:"):
    if len(options) < 1:
        raise ValueError
    info(tip)
    while True:
        for index, item in enumerate(options):
            putchars('  [', style_output(index, fg="bright_white", bold=True, underline=True),']: ', style_output(item, fg='bright_white'), for_color=True, newline=True)
        num = input('> ', filter=__CHOICE_FILTER_BUILDER(*tuple(map(str, range(len(options))))), min=1, max=len(str(len(options))))
        num = int(num)
        if 0 <= num < len(options):
            return num
        error('ERROR: Please choose one of these items!')