#!/usr/bin/python3

import os
from random import choice
from string import ascii_lowercase
from urllib import request,error

def createFd():
    print("Creating anonymous fd")
    s = ""
    for _ in range(7):
        s += choice(ascii_lowercase)

    fd = os.memfd_create(s,0)
    if fd == -1:
        print("Error in creating fd")
        exit(0)
    return fd

def writeToFile(fd,c):
    print("Writing contents to anonymous file")
    with open("/proc/self/fd/{}".format(fd),'wb') as f:
        f.write(c)

def execAnonFile(fd,args,wait_for_proc_terminate):
    print("Spawning process...")
    child_pid = os.fork()
    if child_pid == -1:
        print("Error spawning new process")
        exit()
    elif child_pid == 0:
        print("[+] Executing...")
        fname = "/proc/self/fd/{}".format(fd)
        args.insert(0,fname)
        os.execve(fname,args,dict(os.environ))        
    else:
        if wait_for_proc_terminate:
            print("Waiting for new process ({}) to terminate".format(child_pid))
            os.waitpid(child_pid,0)
        else:
            print("New process is now orphaned")

# MAIN CODE
elf_contents = b"" # ELF contents, example format: b"\x23\x57..."
args = [] # List of arguments to pass to program
wait_for_proc_terminate = True # Wait for new spawned process to terminate

try:
    fd = createFd()
    writeToFile(fd,elf_contents)
    execAnonFile(fd,args,wait_for_proc_terminate)
except KeyboardInterrupt:
    print("User interrupted!")