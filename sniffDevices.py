from ipaddress import IPv4Network
from threading import Thread
from socketserver import _Threads as Threads
from ping3 import ping
import socket
myself = socket.gethostbyname(socket.gethostname())
MASK = '255.255.255.0'
network = IPv4Network(myself+'/'+MASK, strict=False)
l = []
def go(i):
    try:
        n = ping(str(i), timeout=2, size=32)
    except:
        return
    if n:
        l.append(str(i))
threads = Threads()
networks = list(network)[2:-1]
for i in networks:
    thread = Thread(target=go, args=(i, ))
    thread.start()
    threads.append(thread)
threads.join()
n = len(l)
print('There', 'are' if n>1 else 'is', n, 'device'+('s' if n>1 else ''), 'connected to your router:')
for i in l:
    fqdn = socket.gethostbyname()
    print(i, end='')
    if i == myself:
        print(' [ME]')
    else:
        print()