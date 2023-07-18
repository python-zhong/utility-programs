from socket import *
from click import style
try:
    from ctypes import windll
except:
    raise RuntimeError('Failed to load WinDLL. Perhaps this program is not running from windows?') from None
from shutil import get_terminal_size


# Check Administrator
if not windll.shell32.IsUserAnAdmin():
    print('Error: Requires Administrator!')
    n = input('Elevate? [y/N]: ')
    if n.strip().lower() == 'y':
        try:
            from sys import executable
            from win32api import ShellExecute
            from shutil import which
            if path := which('wt'): # Check Windows Terminal
                ShellExecute(
                    None,
                    'runas',
                    path,
                    f'"{executable}" "{__file__}"',
                    None,
                    3
                )
            else: # conhost
                ShellExecute(
                    None,
                    'runas',
                    executable,
                    f'"{__file__}"',
                    None,
                    3
                )
        except Exception as e:
            print('Elevate Failed. Please install `pywin32` module.')
            print(e.__class__.__name__+(':' if e.args is not None and len(e.args) >= 1 else ''), ''.join(map(str, e.args) if e.args is not None else ()))
    exit(0)
# Colorful Format
RETURN = '↲'
SPACE = '·'
BACKSPACE = '←'
HT = '→'
VT = '↓'


def decoder(bts):
    decoded = ''
    echoable = range(0x20, 0x7E + 1)
    for i in bts:
        if i not in echoable:
            if chr(i) == '\r':
                decoded += chr(i)
                continue
            elif chr(i) == '\n':
                if len(decoded) < 2:
                    decoded = style(RETURN, fg=(100, 100, 100)) + '\n'
                elif decoded[-1] == '\r':
                    decoded = decoded[:-1] + style(RETURN, fg=(100, 100, 100)) + '\n'
                else:
                    decoded += style(RETURN, fg=(100, 100, 100)) + '\n'
                continue
            elif chr(i) == '\v':
                decoded += style(VT, fg=(100, 100, 100)) + '\v'
                continue
            elif chr(i) == '\t':
                decoded += style(HT, fg=(100, 100, 100)) + '\t'
                continue
            elif chr(i) == '\b':
                decoded += style(BACKSPACE, fg=(100, 100, 100))
                continue
            i = hex(i)[2:].upper()
            if len(i) < 1:
                i = '00'
            elif len(i) < 2:
                i = '0' + i
            char = '\\x' + i
            char = style(char, fg='red')
        else:
            char = chr(i)
            if char == ' ':
                char = style('·', fg=(100, 100, 100))
            else:
                char = style(char, fg='green')
        decoded += char
    return decoded

# Create Listen Socket
HOST = gethostbyname(gethostname())
s = socket(AF_INET, SOCK_RAW, IPPROTO_IP)
# Bind socket to Local Computer
s.bind((HOST, 0))
# Config socket and start listening
s.setsockopt(IPPROTO_IP, IP_HDRINCL, 1)
s.ioctl(SIO_RCVALL, RCVALL_ON)

# Start Receiving!
while True:
    try:
        data, addr = s.recvfrom(65565)
        host, port = addr
        data = decoder(data)
        n = get_terminal_size().columns
        left = n - len(f'RECEIVED FROM {host}:{port} ')
        print(style('RECEIVED FROM', fg='cyan', bg='white') + style(' ', bg='white') + style(f'{host}', fg='green', bg='white', bold=True) + style(':', bg='white', fg='yellow') + style(f'{port}', fg='blue', bg='white', bold=True) + style(' ' + '*' * left, bg='white', fg='magenta'))
        print(data)
    except KeyboardInterrupt:
        break

# Stop Listening
s.ioctl(SIO_RCVALL, RCVALL_OFF)
