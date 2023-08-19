from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import showerror, showwarning
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askopenfilename
from os import path, environ
from subprocess import run
from json import loads
from locale import getencoding
from threading import Thread
try:
    import ctypes; ctypes.oledll.shcore.SetProcessDpiAwareness(1)
except: pass
tk = Tk(className='exporter')
tk.title('PE Dumper')
tk.resizable(False, False)
ufm = Frame(tk)
ufm.pack(side=TOP, fill=X)
dfm = Frame(tk)
dfm.pack(side=BOTTOM, fill=X)
Label(ufm, text='`dumpbin.exe` path:').pack(side=LEFT)
pth = Label(ufm, foreground='green', justify=CENTER, relief=SOLID)
pth.pack(side=LEFT, padx=5)
Button(dfm, text='Exit', command=tk.destroy).pack(side=RIGHT)
Exceptions = {
    'VSWHERE_NOT_FOUND' : "ERROR: Failed to find dumpbin.exe automatically:\n"
                          "       Couldn't find `vswhere.exe` on your computer.\n"
                          "       Maybe you don't install Visual Studio on your computer.\n"
                          "       `dumpbin.exe` usually installed with Visual Studio when you choice the `C/C++` Tookit on the Installation Page.",
    'VSDEVCMD_NOT_FOUND': "WARNING: Failed to find dumpbin.exe on Visual Studio version %s:\n"
                          "         Couldn't find `VsDevCmd.bat` on your computer.\n"
                          "         Check your Visual Studio Installation.",
    'VSDEVCMD_FAILED'   : "WARNING: Failed to gather information with `VsDevCmd.bat`.",
    'DUMPBIN_NOT_FOUND' : "ERORR: Can't find any dumpbin.exe on your Visual Studio."
}
titlebar = "%s - PE Dumper"
dumpbins = []
MakeCMD = lambda *commands: ' '.join([f"{i}" if ' ' not in i else f'"{i}"' for i in commands])
def find_dumpbins():
    dumpbins.clear()
    PROGRAMFILESX86 = environ.get("ProgramFiles(x86)", environ.get("ProgramFiles", None))
    if PROGRAMFILESX86:
        VSWHERE = path.join(PROGRAMFILESX86, 'Microsoft Visual Studio', 'Installer', 'vswhere.exe')
        if not path.isfile(VSWHERE):
            showerror(titlebar % "Error", Exceptions['VSWHERE_NOT_FOUND'])
            tk.destroy()
            exit(127)
        else:
            vsinfo = loads(run(MakeCMD(VSWHERE, '-all',  '-prerelease',  '-legacy', '-format' ,'json', '-utf8', '-nocolor'), capture_output=True).stdout)
            for i in vsinfo:
                isnp = i['installationPath']
                vcmd = path.join(isnp, 'Common7', 'Tools', 'VsDevCmd.bat')
                try:
                    p = run(
                        MakeCMD('cmd.exe', '/k', vcmd),
                        capture_output=True,
                        input=b"@echo off\nwhere dumpbin\nexit\n"
                    )
                except OSError:
                    showerror(titlebar % 'Error', Exceptions['VSWHERE_NOT_FOUND'])
                    tk.destroy()
                    exit(127)
                else:
                    w = p.stdout.split(b'\n')[-3].strip().decode(encoding='UTF-8')
                    if path.isfile(w):
                        dumpbins.append(w)
                        continue
                    if p.returncode == 0:
                        showwarning(titlebar % 'Warning', Exceptions['VSDEVCMD_FAILED'])
                        continue
                    showwarning(titlebar % 'Warning', Exceptions['VSDEVCMD_NOT_FOUND'] % i['installationVersion'])
    else:
        showerror(titlebar % 'Error', Exceptions['VSWHERE_NOT_FOUND'])
        tk.destroy()
        exit(127)
current_dumpbin = ''
find_dumpbins()
def choose_dumpbins(refind=True):
    if refind:
        find_dumpbins()
    if len(dumpbins) < 1:
        showerror(titlebar % 'Error', Exceptions['DUMPBIN_NOT_FOUND'])
        tk.destroy()
        exit(127)
    current_dumpbin = ''
    tp = Toplevel(tk)
    tp.title(titlebar % "Choose `dumpbin.exe`")
    tp.resizable(False, False)
    w = 0
    for i in dumpbins:
        if len(i) > w:
            w = len(i)
    Label(tp, text="We found these `dumpbin.exe` on your computer. Choose one from the box.").pack(side=TOP)
    ls = Listbox(tp, width=w, activestyle=DOTBOX)
    ls.pack(side=TOP)
    ls.insert(END, *dumpbins)
    def ondestory(_=None):
        tp.grab_release()
        tp.destroy()
    def fulldestory():
        ondestory()
        tk.destroy()
    Button(tp, text='Exit', command=fulldestory).pack(side=BOTTOM)
    tp.transient(tk)
    tp.grab_set()
    def onselect(_=None):
        nonlocal current_dumpbin
        selection = ls.curselection()
        if len(selection) < 1:
            return
        current_dumpbin = dumpbins[selection[0]]
        pth.config(text=current_dumpbin)
        ondestory()
    ls.bind("<Double-ButtonPress>", onselect)
    tp.protocol("WM_DELETE_WINDOW", ondestory)
    tp.mainloop()
    return current_dumpbin
if len(dumpbins) < 1:
    showerror(titlebar % 'Error', Exceptions['DUMPBIN_NOT_FOUND'])
    tk.destroy()
    exit(127)
elif len(dumpbins) > 1:
    current_dumpbin = choose_dumpbins(refind=False)
else:
    current_dumpbin = dumpbins[0]
    pth.config(text=current_dumpbin)
Button(ufm, text='Switch `dumpbin.exe`', command=choose_dumpbins).pack(side=RIGHT)
def remove_banner(inp: str, remove_summary=True, keep_lhead=False):
    inp = inp.strip()
    n = [i.rstrip() for i in inp.split('\n')][4 if not remove_summary else 7 if not keep_lhead else 6:]
    if not n[0].strip() and remove_summary:
        try:
            i = n.index('  Summary')
            n = n[1:i]
        except ValueError:
            pass
    return '\n'.join(n).strip()
def runDumpbin(file, *cmd, isSummary=False, keep_lhead=False):
    try:
        tk.update()
        p = run(MakeCMD(current_dumpbin, file, *cmd), capture_output=True)
        tk.update()
    except OSError:
        showerror(titlebar % 'Error', 'Failed to open process')
    else:
        info = p.stdout.decode(encoding=getencoding(), errors='backslashreplace')
        if p.returncode != 0:
            showerror(titlebar % 'Error', '`dumpbin` exited, status %d.\n%s' % (p.returncode, remove_banner(info, remove_summary=True)))
        else:
            return remove_banner(info, not isSummary, keep_lhead)        
def dump():
    f = askopenfilename(title='Open ...', filetypes=[
        ('Supported PE Files', ('*.exe', '*.dll', '*.pyd', '*.sys', '*.efi', '*.cpl', '*.scr', '*.ocx', '*.mui')),
        ('Executables', ('*.exe', '*.sys', '*.scr')),
        ('Dynamic Link Libraries', ('*.dll', '*.pyd', '*.efi', '*.cpl', '*.ocx', '*.mui')),
        ('Executable Image Files', '*.exe'),
        ('Dynamic Link Library (DLL) Files', '*.dll'),
        ('Python Extension Module Files', '*.pyd'),
        ('Drivers', '*.sys'),
        ('UEFI Bootable Files', '*.efi'),
        ('Control Panel Items', '*.cpl'),
        ('ActiveX Controls', '*.ocx'),
        ('Localized Resource', '*.mui'),
        ('All Files', '*.*')
    ])
    if path.isfile(f):
        def update_view():
            while True:
                try:
                    tk.update()
                    tp.update()
                except:
                    break
        Thread(target=update_view).run()
        tp = Toplevel(tk)
        tp.resizable(False, False)
        tp.title('Dumping file "%s" ...' % f)
        tp.update()
        fm = Frame(tp)
        fm.pack(side=TOP, fill=BOTH)
        pgs = Progressbar(tp, orient=HORIZONTAL, mode='determinate', maximum=1)
        pgs.pack(side=TOP, fill=X)
        tvf = Frame(fm)
        tvf.pack(side=LEFT, fill=BOTH)
        tv = Treeview(tvf, height=30, selectmode=BROWSE, show='tree')
        tv.pack(side=LEFT, fill=BOTH)
        sb = Scrollbar(tvf, orient=VERTICAL, command=tv.yview)
        sb.pack(side=RIGHT, fill=Y)
        tv.config(yscrollcommand=sb.set)
        stf = Frame(fm)
        stf.pack(side=RIGHT, fill=BOTH)
        st = ScrolledText(stf, width=150, height=36, wrap='none')
        st.pack(side=TOP, fill=BOTH)
        sbt = Scrollbar(stf, orient=HORIZONTAL, command=st.xview)
        sbt.pack(side=BOTTOM, fill=X)
        st.config(xscrollcommand=sbt.set)
        st.insert(END, 'Dumping, please wait ...\nReading Summary ...')
        st.tag_add('tag', '1.0', '2.0')
        st.tag_config('tag', foreground='#808080')
        st.tag_add('tag1', '2.0', END)
        st.tag_config('tag1', foreground='#505050')
        st.config(state=DISABLED)
        def update_text(text):
            st.config(state=NORMAL)
            st.delete('2.0', END)
            st.tag_delete('tag1')
            st.insert(END, '\n'+text)
            st.tag_add('tag1', '2.0', END)
            st.tag_config('tag1', foreground='#505050')
            st.config(state=DISABLED)
        summary = runDumpbin(f, '/summary', isSummary=True)
        if summary is None:
            return tp.destroy()
        pgs.step(1/14)
        update_text('Reading Archive Members ...')
        archivemembers = runDumpbin(f, '/archiveMembers')
        if archivemembers is None:
            return tp.destroy()
        pgs.step(1/14)
        update_text('Reading CLR Header ...')
        clrheader = runDumpbin(f, '/clrHeader')
        if clrheader is None:
             return tp.destroy()
        pgs.step(1/14)
        update_text('Reading Dependents ...')
        dependents = runDumpbin(f, '/dependents')
        if dependents is None:
            return tp.destroy()
        pgs.step(1/14)
        update_text('Reading Directives ...')
        directives = runDumpbin(f, '/directives')
        if directives is None:
            return tp.destroy()
        pgs.step(1/14)
        update_text('Reading Exports ...')
        exports = runDumpbin(f, '/exports')
        if exports is None:
            return tp.destroy()
        pgs.step(1/14)
        update_text('Reading FPO ...')
        fpo = runDumpbin(f, '/fpo')
        if fpo is None:
            return tp.destroy()
        pgs.step(1/14)
        update_text('Reading Headers ...')
        headers = runDumpbin(f, '/headers', keep_lhead=True)
        if headers is None:
            return tp.destroy()
        pgs.step(1/14)
        update_text('Reading Imports ...')
        imports = runDumpbin(f, '/imports')
        if imports is None:
            return tp.destroy()
        pgs.step(1/14)
        update_text('Reading Relocations ...')
        relocations = runDumpbin(f, '/relocations')
        if relocations is None:
            return tp.destroy()
        pgs.step(1/14)
        update_text('Reading Symbols ...')
        symbols = runDumpbin(f, '/symbols')
        if symbols is None:
            return tp.destroy()
        pgs.step(1/14)
        update_text('Reading TLS ...')
        tls = runDumpbin(f, '/tls')
        if tls is None:
            return tp.destroy()
        pgs.step(1/14)
        update_text('Reading Unwind Info ...')
        unwindinfo = runDumpbin(f, '/unwindinfo')
        if unwindinfo is None:
            return tp.destroy()
        pgs.config(value=1)
        tp.title('Dump of file "%s"' % f)
        st.config(state=NORMAL)
        st.delete('1.0', END)
        st.tag_delete('tag1')
        st.tag_delete('tag')
        st.insert('1.0', 'Select One Item')
        st.tag_add('tag', '1.0', END)
        st.tag_config('tag', foreground='#808080')
        st.config(state=DISABLED)
        Button(tp, text='Close', command=tp.destroy).pack(side=BOTTOM)
        n = {}
        riid = tv.insert('', END, text='Dump Info', open=True)
        n[riid] = "Select One Item"
        n[tv.insert(riid, END, text='Summary')] = summary
        n[tv.insert(riid, END, text='Archive Members')] = archivemembers
        n[tv.insert(riid, END, text='CLR Header')] = clrheader
        n[tv.insert(riid, END, text='Dependents')] = dependents
        n[tv.insert(riid, END, text='Directives')] = directives
        n[tv.insert(riid, END, text='Exports')] = exports
        n[tv.insert(riid, END, text='FPO')] = fpo
        n[tv.insert(riid, END, text='Headers')] = headers
        n[tv.insert(riid, END, text='Imports')] = imports
        n[tv.insert(riid, END, text='Relocations')] = relocations
        n[tv.insert(riid, END, text='Symbols')] = symbols
        n[tv.insert(riid, END, text='TLS')] = tls
        n[tv.insert(riid, END, text='Unwind Info')] = unwindinfo
        tag_flag = True
        def onselect(_=None):
            nonlocal tag_flag
            selection = tv.selection()
            st.config(state=NORMAL)
            st.delete('1.0', END)
            if tag_flag:
                st.tag_delete('tag')
                tag_flag = False
            if len(selection) < 1:
                st.insert('1.0', 'Choose One Item')
            else:
                content = n[selection[0]].strip()
                if content:
                    st.insert(END, content)
                    if selection[0] == riid:
                        tag_flag = True
                else:
                    tag_flag = True
                    st.insert(END, "<No Information>")
                if tag_flag:
                    st.tag_add('tag', '1.0', END)
                    st.tag_config('tag', foreground='#808080')
            st.config(state=DISABLED)
        tv.bind("<<TreeviewSelect>>", onselect)
        tp.mainloop()
Button(dfm, text='Dump', command=dump).pack(side=LEFT)
style = Style(tk)
style.configure('Treeview', rowheight=25)
tk.mainloop()
