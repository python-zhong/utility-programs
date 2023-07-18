from flask import Flask, request
from socket import gethostname, gethostbyname
from os import path
from argparse import ArgumentParser

app = Flask(__name__)
page = """\
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Upload</title>
    </head>
    <body>
        <h1>Upload</h1>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit" value="Upload">
        </form>
    </body>
</html>
"""


@app.route('/')
def sendpage():
    return page


@app.route('/upload', methods=['POST'])
def process():
    try:
        file = request.files['file']
        file.save(path.join(upload_path, file.filename))
        return '<script>window.onload=function(){alert("Success");location.href="/";}</script>'
    except:
        return '<script>window.onload=function(){alert("Failed");location.href="/";}</script>'


if __name__ == '__main__':
    parser = ArgumentParser(description='Light web File Transfer')
    parser.add_argument(
        '-a', '--address', '--host',
        help='Specify the host. Set it to 0.0.0.0 [default] to bind all addresses.',
        dest='hostname',
        default='0.0.0.0'
    )
    def port(n):
        n = int(n)
        if not 0 <= n <= 65535:
            raise ValueError('Not a valid port')
        return n
    parser.add_argument(
        '-p', '--port',
        help='Specify the port. Must be an integer between 0 and 65535. Default 5000.',
        default=5000,
        type=port
    )
    def directory(p):
        if not path.isdir(p):
            raise ValueError('Not a directory')
        return p
    parser.add_argument(
        'path',
        help='Path to save uploaded file',
        type=directory
    )
    ns = parser.parse_args()
    upload_path = ns.path
    ip = ns.hostname
    port = ns.port
    app.run(host=ip, port=ns.port)
