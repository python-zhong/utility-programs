from flask import Flask, send_from_directory, render_template_string, Response
from os import getcwd, path as fs, listdir, fspath
from uuid import uuid1
from pathlib import WindowsPath as _Path, PurePosixPath as URLPath
from argparse import ArgumentParser
from time import strftime, localtime
def express_size(size: int, prec: int=2) -> str:
    KB = 2 ** 10
    MB = 2 ** 20
    GB = 2 ** 30
    TB = 2 ** 40
    PB = 2 ** 50
    EB = 2 ** 60
    ZB = 2 ** 70
    YB = 2 ** 80
    def my_round(n):
        if not prec:
            return int(n)
        return round(n, prec)
    num = 0
    target = ''
    if size < KB:
        num = size
        target = f'Byte{"s" if size > 1 else ""}'
    elif size < MB:
        num = my_round(size / KB)
        target = 'KB'
    elif size < GB:
        num = my_round(size / MB)
        target = 'MB'
    elif size < TB:
        num = my_round(size / GB)
        target = 'GB'
    elif size < PB:
        num = my_round(size / TB)
        target = 'TB'
    elif size < EB:
        num = my_round(size / PB)
        target = 'PB'
    elif size < ZB:
        num = my_round(size / EB)
        target = 'EB'
    elif size < YB:
        num = my_round(size / ZB)
        target = 'ZB'
    else:
        num = my_round(size / YB)
        target = 'YB'
    return f'{num} {target}'
gettime = lambda t: strftime('%Y-%m-%d %H:%M:%S', localtime(t))
app = Flask('FTP Mini')
folder_html = """<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8" name="viewport" content="width=device-width;">
        <title>FTP Mini: {{ path }}</title>
        <style>
            html {
                font-family: 'Cascadia Code', Consolas, 'Courier New', monospace;
            }
            a {
                color: dodgerblue;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
            .path {
                padding-left: 2px;
            }
        </style>
    </head>
    <body>
        <h1>FTP Mini</h1>
        <p style="display: flex;">
            Path:&nbsp;
            {% for parent in parents %}
                <a href="{{ parent.path }}" class="path">{{ parent.name }}/</a>
            {% endfor %}
        </p>
        {% if not isRoot %}
        <a href="{{ parent }}">&lt;&lt; Parent Folder</a>
        {% endif %}
        <table border="1" width="100%">
            <thead>
                <tr>
                    <td>Name</td>
                    <td>Type</td>
                    <td>Size</td>
                    <td>Access Time</td>
                    <td>Create Time</td>
                    <td>Modify Time</td>
                </tr>
            </thead>
            <tbody>
                {% for item in items %}
                    <tr>
                        <td>
                            <a href="{{ item.path }}">{{ item.name }}</a>
                        </td>
                        <td>{{ item.type }}</td>
                        <td>{{ item.size }}</td>
                        <td>{{ item.atime }}</td>
                        <td>{{ item.ctime }}</td>
                        <td>{{ item.mtime }}</td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    </body>
</html>"""
class Path(_Path):
    @property
    def listdir(self) -> list["Path"]:
        ls = listdir(self)
        l = []
        for item in ls:
            l.append(self.joinpath(item))
        return l
    @property
    def size(self):
        return fs.getsize(self)
    @property
    def atime(self):
        return fs.getatime(self)
    @property
    def ctime(self):
        return fs.getctime(self)
    @property
    def mtime(self):
        return fs.getmtime(self)
@app.route('/')
def parent():
    ld = path.listdir
    ld.sort(key=lambda k: fspath(k).lower())
    folders = []
    files = []
    for l in ld:
        if l.is_dir():
            folders.append({'name': l.name, 'path': fspath(URLPath('/').joinpath(l.name)), 'type': 'Folder', 'size': '-', 'atime': gettime(l.atime), 'ctime': gettime(l.ctime), 'mtime': gettime(l.mtime)})
        else:
            files.append({'name': l.name, 'path': fspath(URLPath('/').joinpath(l.name)), 'type': 'File', 'size': express_size(l.size), 'atime': gettime(l.atime), 'ctime': gettime(l.ctime), 'mtime': gettime(l.mtime)})
    folders.sort(key=lambda k: k['name'].lower())
    files.sort(key=lambda k: k['name'].lower())
    return render_template_string(folder_html, path='/', parents=[{'name': '', 'path': '/'}], isRoot=True, items=folders+files)
@app.route('/<path:filename>')
def child(filename):
    upath = URLPath(filename)
    real = path.joinpath(upath)
    try:
        if real.is_file():
            return send_from_directory(path, upath)
        elif real.is_dir():
            ld = real.listdir
            ld.sort(key=lambda k: fspath(k).lower())
            folders = []
            files = []
            for l in ld:
                if l.is_dir():
                    folders.append({'name': l.name, 'path': '/'+fspath(upath.joinpath(l.name)).strip('/'), 'type': 'Folder', 'size': '-', 'atime': gettime(l.atime), 'ctime': gettime(l.ctime), 'mtime': gettime(l.mtime)})
                else:
                    files.append({'name': l.name, 'path': '/'+fspath(upath.joinpath(l.name)).strip('/'), 'type': 'File', 'size': express_size(l.size), 'atime': gettime(l.atime), 'ctime': gettime(l.ctime), 'mtime': gettime(l.mtime)})
            folders.sort(key=lambda k: k['name'].lower())
            files.sort(key=lambda k: k['name'].lower())
            p = list(upath.parents)
            p.reverse()
            p.append(upath)
            parents = [{'name': parent.name, 'path': '/'+fspath(parent) if len(fspath(parent)) > 1 else '/'} for parent in p]
            return render_template_string(folder_html, path='/', parents=parents, isRoot=False, items=folders+files, parent=parents[-2]['path'])
        else:
            return Response(f'<span style="color: red;">ERROR:</span> Not a file or directory: {filename}', status=404)
    except Exception as e:
        name = e.__class__.__name__
        reason = '<Unknown Reason>'
        if e.args is not None:
            reason = ''.join(map(str, e.args))
        return Response(f'<span style="color: red;">ERROR ({name}):</span>{reason}', status=500)
if __name__ == '__main__':
    parser = ArgumentParser(description='Simple FTP (mini)')
    parser.add_argument('--path', help='Which path to serve', default=getcwd().replace('\\', '/'))
    parser.add_argument('--host', help="Server's host", default='127.0.0.1')
    parser.add_argument('--port', help="Server's port", type=int, default=5000)
    args = parser.parse_args()
    path = Path(args.path)
    if not path.is_dir():
        parser.error(f'Invalid Path: "{args.path}"')
    port = args.port
    if port <= 0 or port > 65535:
        parser.error(f'Invalid Port: {args.port}')
    host = args.host
    print('Serving FTP:', path)
    app.run(host=host, port=port)
