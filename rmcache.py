from os.path import isdir
from os import listdir, getcwd  #, remove
from shutil import rmtree
from argparse import ArgumentParser
from pathlib import Path
def delete(path: str):
    if not isdir(path):
        print(f'Err: No such file or dictionary: "{path}"')
        return 0, 0
    path = path if path.endswith('/') else path + '/'
    success = 0
    failed = 0
    information = listdir(path)
    for i in information:
        p = path + i
        if isdir(p):
            if i == '__pycache__':
                print(f'Deleting cache folder "{p}" ...', end=' ')
                try:
                    c = len(listdir(p))
                except:
                    c = 1
                try:
                    rmtree(p)
                    print('Done.')
                    success += c
                except:
                    print('Failed.')
                    failed += c
            else:
                s, f = delete(p)
                success += s
                failed += f
    return success, failed
def main(p=None):
    if p is None:
        from sys import path as p
    s = f = 0
    last_searched: Path = None
    p.sort()
    for i in p:
        if i == '.':
            i = getcwd()
        current = Path(i)
        if not isdir(i):
            continue
        if last_searched is not None:
            if current.is_relative_to(last_searched):
                continue
        print(f'Detecting Path "{i}" ...')
        a, b = delete(i)
        s += a
        f += b
        print('Success to delete', a, 'files. Failed to delete', b, 'files.')
        last_searched = current
    print('Process finished. Deleted', s, 'files. Failed to delete', b, 'files.')
    return 0
if __name__ == '__main__':
    parser = ArgumentParser(description='Clean .pyc files', epilog='Default, clean all caches in <sys.path>.')
    parser.add_argument('-s', '--scan', help='Scan and remove .pyc files in specific folder.', default=None, nargs='*')
    args = parser.parse_args()
    main(args.scan)