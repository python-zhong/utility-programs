import os
import typing as t

if os.name != 'nt':
    raise RuntimeError('ShellExecute.py ONLY support Windows')
try:
    import ctypes
    from ctypes import wintypes
    shell32 = ctypes.WinDLL('shell32.dll')
    _ShellExecute = shell32.ShellExecuteA
    _ShellExecute.restype = wintypes.HINSTANCE
    _ShellExecute.argtypes = (
        wintypes.HWND,
        wintypes.LPCSTR,
        wintypes.LPCSTR,
        wintypes.LPCSTR,
        wintypes.LPCSTR,
        wintypes.INT
    )
    _IsUserAnAdmin = shell32.IsUserAnAdmin
    _IsUserAnAdmin.restype = ctypes.c_bool
except (OSError, AttributeError, ImportError) as e:
    raise RuntimeError('Failed to load shell32.dll') from e
SW_HIDE = 0
SW_SHOWNORMAL = SW_NORMAL = 1
SW_SHOWMINIMIZED = 2
SW_SHOWMAXIMIZED = SW_MAXIMIZE = 3
SW_SHOWNOACTIVATE = 4
SW_SHOW = 5
SW_MINIMIZE = 6
SW_SHOWMINNOACTIVE = 7
SW_SHOWNA = 8
SW_RESTORE = 9
SW_SHOWDEFAULT = 10
SW_FORCEMINIMIZE = 11

_TEXT = t.Union[str, bytes]
def ShellExecute(
    lpFile: _TEXT,
    nShowCmd: int,
    hwnd: t.Optional[wintypes.HWND] = None,
    lpParameters: t.Optional[t.Union[t.Iterable[_TEXT], _TEXT]] = None,
    lpDirectory: t.Optional[_TEXT] = None,
    lpOperation: t.Optional[_TEXT] = None,
) -> int:
    if isinstance(lpFile, str):
        lpFile = lpFile.encode()
    elif not isinstance(lpFile, bytes):
        raise TypeError('Invalid argument `lpFile`: Must be str or int')
    if not isinstance(nShowCmd, int):
        raise TypeError('Invalid argument `nShowCmd`: Must be one of SW_* constants')
    elif nShowCmd not in range(0, 12):
        raise ValueError('Invalid argument `nShowCmd`: Must be one of SW_* constants')
    if hwnd is not None:
        if not isinstance(hwnd, wintypes.HWND):
            raise ValueError('Invalid argument `hwnd`: Must be ctypes.HWND or None')
    if lpParameters is not None:
        if isinstance(lpParameters, str):
            lpParameters = lpParameters.encode()
        elif isinstance(lpParameters, t.Iterable):
            lpParameters = tuple(lpParameters)
            p = b''
            for parameter in lpParameters:
                if isinstance(parameter, str):
                    parameter = parameter.encode()
                elif not isinstance(parameter, bytes):
                    raise TypeError('Invalid argument `lpParameters`: Must be str, bytes, or Iterable that contains str or bytes')
                p += b'"%s"' % parameter + b' '
            lpParameters = p[:-1]
        elif not isinstance(lpParameters, bytes):
            raise TypeError('Invalid argument `lpParameters`: Must be str, bytes, or Iterable that contains str or bytes')
    if lpDirectory is not None:
        if isinstance(lpDirectory, str):
            lpDirectory = lpDirectory.encode()
        elif not isinstance(lpDirectory, bytes):
            raise TypeError('Invalid argument `lpDirectory`: Must be str or bytes')
    if lpOperation is not None:
        if isinstance(lpOperation, str):
            lpOperation = lpOperation.encode()
        elif not isinstance(lpOperation, bytes):
            raise TypeError('Invalid argument `lpOperation`: Must be str or bytes')
    return _ShellExecute(hwnd, lpOperation, lpFile, lpParameters, lpDirectory, nShowCmd)
def IsUserAnAdmin():
    return _IsUserAnAdmin()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser('python -m Packages.shell', description='ShellExecute Helper')
    parser.add_argument(
        '-s', '--show-cmd',
        help='Show the Console Host (nShowCmd=SW_SHOW)',
        action='store_true',
        dest='showCmd'
    )
    parser.add_argument(
        '-d', '--working-directory', '--directory', '--workdir',
        help='Set the working directory.',
        dest='workDir'
    )
    parser.add_argument(
        '-o', '--operation',
        choices=['edit', 'explore', 'find', 'open', 'print', 'runas'],
        help='The operation verb to execute',
        dest='operation'
    )
    parser.add_argument(
        '-a', '--args',
        help='Arguments to the operation',
        dest='args'
    )
    parser.add_argument('file', help='The file path')
    res = parser.parse_args()
    ShellExecute(res.file, SW_SHOW if res.showCmd else SW_HIDE, lpParameters=res.args, lpDirectory=res.workDir, lpOperation=res.operation)