from enum import Enum
from warnings import warn
warn("This module is Experimental")
from sys import platform
if platform == 'win32':
    from ._colorama import fix_windows_console
    fix_windows_console()
from ._colorama import CSI, OSC
def putbackspace(n=1):
    print('\b'*n, end='')
def erase_back_chars(n=1):
    print('\b \b'*n, end='')
def putnewline(n=1):
    print("\n"*n, end="")
class CursorOp(Enum):
    MoveUp = 'A'
    MoveDown = 'B'
    MoveForeword = 'C'
    MoveBack = 'D'
    MoveNextLine = 'E'
    MoveCurLn = 'F'
    MoveHoriAbs = 'G'
    MoveVertAbs = 'd'
    MovePos = 'H'
    MoveHoriVertPos = 'f'
    ANSISYSSC = 's'
    ANSISYSRC = 'u'
def move_cursor(op: CursorOp, a=None, b=None, /):
    cmd = CSI
    if a:
        cmd += str(a)
    if b:
        cmd += ';' + str(b)
    cmd += op.value
    print(cmd, end="")
def set_cursor_blinking(state):
    if state:
        print(CSI + '?12h', end="")
    else:
        print(CSI + '?12l', end="")
def set_cursor_visibility(state):
    if state:
        print(CSI + '?25h', end="")
    else:
        print(CSI + '?25l', end="")

class CursorShape(Enum):
    Default = 0
    BlinkingBlock = 1
    SteadyBlock = 2
    BlinkingUnderline = 3
    SteadyUnderline = 4
    BlinkingBar = 5
    SteadyBar = 6
def set_cursor_shape(shape: CursorShape):
    print(CSI + str(shape.value) + 'SP q')

def scroll_view_up(n=1):
    print(CSI + str(n) + 'S', end="")
def scroll_view_down(n=1):
    print(CSI + str(n) + 'T', end="")
def insert_n_char(n):
    print(CSI + str(n) + '@', end="")
def delete_n_char(n):
    print(CSI + str(n) + 'P', end="")
def erase_n_char(n):
    print(CSI + str(n) + 'X', end="")
def insert_n_line(n=1):
    print(CSI + str(n) + 'L', end="")
def delete_n_line(n=1):
    print(CSI + str(n) + 'M', end="")
def erase_n_in_display(n):
    print(CSI + str(n) + 'J', end="")
def erase_n_in_line(n=1):
    print(CSI + str(n) + 'K', end="")
def set_console_out_format(
        fg=None, bg=None,
        bold=None, dim=None, underline=None, overline=None, italic=None,
        blink=None,reverse=None, strikethrough=None
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
    _ansi_reset_all = f"{CSI}0m"
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
            bits.append(f"{CSI}{_interpret_color(fg)}m")
        except KeyError:
            raise TypeError(f"Unknown color {fg!r}") from None
    if bg:
        try:
            bits.append(f"{CSI}{_interpret_color(bg, 10)}m")
        except KeyError:
            raise TypeError(f"Unknown color {bg!r}") from None
    if bold is not None:
        bits.append(f"{CSI}{1 if bold else 22}m")
    if dim is not None:
        bits.append(f"{CSI}{2 if dim else 22}m")
    if underline is not None:
        bits.append(f"{CSI}{4 if underline else 24}m")
    if overline is not None:
        bits.append(f"{CSI}{53 if overline else 55}m")
    if italic is not None:
        bits.append(f"{CSI}{3 if italic else 23}m")
    if blink is not None:
        bits.append(f"{CSI}{5 if blink else 25}m")
    if reverse is not None:
        bits.append(f"{CSI}{7 if reverse else 27}m")
    if strikethrough is not None:
        bits.append(f"{CSI}{9 if strikethrough else 29}m")
    print("".join(bits), end="")
def reset_console_out_format():
    print(CSI + "0m", end="")
def format_text(
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
    _ansi_reset_all = f"{CSI}0m"
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
            bits.append(f"{CSI}{_interpret_color(fg)}m")
        except KeyError:
            raise TypeError(f"Unknown color {fg!r}") from None
    if bg:
        try:
            bits.append(f"{CSI}{_interpret_color(bg, 10)}m")
        except KeyError:
            raise TypeError(f"Unknown color {bg!r}") from None
    if bold is not None:
        bits.append(f"{CSI}{1 if bold else 22}m")
    if dim is not None:
        bits.append(f"{CSI}{2 if dim else 22}m")
    if underline is not None:
        bits.append(f"{CSI}{4 if underline else 24}m")
    if overline is not None:
        bits.append(f"{CSI}{53 if overline else 55}m")
    if italic is not None:
        bits.append(f"{CSI}{3 if italic else 23}m")
    if blink is not None:
        bits.append(f"{CSI}{5 if blink else 25}m")
    if reverse is not None:
        bits.append(f"{CSI}{7 if reverse else 27}m")
    if strikethrough is not None:
        bits.append(f"{CSI}{9 if strikethrough else 29}m")
    bits.append(text)
    if reset:
        bits.append(_ansi_reset_all)
    return "".join(bits)
def set_screen_color_palette(i, r, g, b):
    print(OSC + f"4;{i};rgb:{r}/{g}/{b}\033\x5c", end="")
def enable_keypad_app_mode():
    print('\033=', end="")
def enable_keypad_num_mode():
    print('\033>')
def set_cursor_keys_app_mode(state):
    if state:
        print(CSI + '?1h', end="")
    else:
        print(CSI + '?1l', end="")
def report_cursor_position():
    print(CSI + '6n', end="")
def report_device_attrs():
    print(CSI + '0c', end="")
def hori_tab_set():
    print('\033H', end="")
def cursor_hori_tab(n=1):
    print(CSI + str(n) + 'I', end='')
def cursor_back_tab(n=1):
    print(CSI + str(n) + 'Z', end='')
def clear_tab_curcol():
    print(CSI + '0g', end='')
def cursor_clear_allcols():
    print(CSI + '3g', end="")
def enable_dec_linedw_mode():
    print('\033(0', end="")
def enable_ascii_mode():
    print('\033(B', end="")
def set_scroll_margin(t, b):
    print(CSI + f'{t};{b}r', end="")
def set_title(title):
    print(OSC + f'2;{title}\x5c')
def use_backup_bufscreen():
    print(CSI + '?1049h', end="")
def use_main_bufscreen():
    print(CSI + '?1049l', end="")
def set_width_col_to_132():
    print(CSI + '?3h', end="")
def set_width_col_to_80():
    print(CSI + '?3l', end="")
def soft_reset():
    print(CSI + '!p', end="")
class SpecKeys(Enum):
    UpArrow = CSI + 'A'
    DownArrow = CSI + 'B'
    RightArrow = CSI + 'C'
    LeftArrow = CSI + 'D'
    Home = CSI + 'H'
    End = CSI + 'F'
    Ctrl_UpArrow = CSI + '1;5A'
    Ctrl_DownArrow = CSI + '1;5B'
    Ctrl_RightArrow = CSI + '1;5C'
    Ctrl_LeftArrow = CSI + '1;5D'
    Ctrl_Space = '\x00'
    Backspace = '\x7f'
    Pause = '\x1a'
    Escape = '\033'
    Insert = CSI + '2~'
    Delete = CSI + '3~'
    PageUp = CSI + '5~'
    PageDown = CSI + '6~'
    F1 = '\033OP'
    F2 = '\033OQ'
    F3 = '\033OR'
    F4 = '\033OS'
    F5 = CSI + '15~'
    F6 = CSI + '17~'
    F7 = CSI + '18~'
    F8 = CSI + '19~'
    F9 = CSI + '20~'
    F10 = CSI + '21~'
    F11 = CSI + '23~'
    F12 = CSI + '24~'
    