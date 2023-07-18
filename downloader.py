from argparse import ArgumentParser
from urllib.request import urlretrieve
from urllib.error import URLError
from click import progressbar, style
from click._termui_impl import ProgressBar
import typing as t
from sys import exit, stderr, stdout
from os import remove
from Packages.win32confix import fix_windows_console
from Packages.utils import express_file_size
def main():
    parser = ArgumentParser(description='Tiny downloader')
    parser.add_argument('url', help='File to download')
    parser.add_argument('dest', help='Path to save the file')
    parser.add_argument('-s', '--silent', help='Do not show anything during download, except error messages', action='store_true')
    n = parser.parse_args()
    url = n.url
    dest = n.dest
    silent = n.silent
    error = False
    if silent:
        try:
            urlretrieve(url, dest)
        except KeyboardInterrupt:
            error = True
        except OSError as e:
            error = True
            if hasattr(e, 'reason'):
                print('\n' + e.__class__.__name__+':', e.reason, file=stderr, end='')
            else:
                print('\n' + e.__class__.__name__ + ':', ''.join(e.args), file=stderr, end='')
    else:
        fix_windows_console()
        print(
            'Downloading from "',
            style(url, fg='blue', bold=True),
            '" to "',
            style(dest, fg='green', bold=True),
            '" ...',
            sep='', file=stdout)
        print(
            'Waiting for server response ...',
            file=stdout
            )
        progress: t.Optional[t.Union[ProgressBar, int]] = None
        def hook(blocks, block_size, total):
            nonlocal progress
            if progress is None and total >= 0:
                progress = progressbar(
                    fill_char=style(' ', bg='blue'),
                    empty_char=style(' ', bg='bright_black'),
                    bar_template=f'Downloading ... |%(bar)s| %(label)s {style("%(info)s", fg="green")}',
                    show_pos=False,
                    show_eta=True,
                    show_percent=False,
                    label='0 Bytes / %.2f %s' % express_file_size(total),
                    length=total,
                    file=stdout
                )
            elif progress is None:
                progress = 0
                print('Downloading ...', end='', file=stdout)
            else:
                if total >= 0:
                    progress.label = (f'{style("%.2f", fg="cyan", bold=True)} {style("%s", fg="blue")} / '
                                      f'{style("%.2f", fg="cyan", bold=True)} {style("%s", fg="blue")} '
                                      f'{style("%d%%", fg="magenta", bold=True)}') % (
                                        express_file_size(block_size*blocks) +
                                        express_file_size(total) +
                                        (int((block_size*blocks)/total*100), )
                                      )
                    progress.update(block_size)
                else:
                    if progress:
                        print('\b'*progress, end='', file=stdout)
                        text = f'{style("%.2f", fg="cyan")} {style("%s", fg="blue")}' % express_file_size(block_size*blocks)
                        print(text, end='', file=stdout)
                        progress = len(text)
        try:
            urlretrieve(url, dest, hook)
        except KeyboardInterrupt:
            print('\nCannelled', end='', file=stderr)
            error = True
        except OSError as e:
            error = True
            if hasattr(e, 'reason'):
                print('\n' + e.__class__.__name__+':', e.reason, file=stderr, end='')
            else:
                print('\n' + e.__class__.__name__ + ':', ''.join(e.args), file=stderr, end='')
        if error:
            try:
                remove(dest)
            except OSError:
                pass
        else:
            if isinstance(progress, ProgressBar):
                progress.render_finish()
            print('Downloaded Successfully', file=stdout, end='')
    return 0
if __name__ == '__main__':
    exit(main())