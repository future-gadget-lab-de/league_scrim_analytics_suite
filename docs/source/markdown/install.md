# Installing LSAS

The first prerequisite is to install Python. In the Windows case, that is enough (see [Python Downloads for Windows](https://www.python.org/downloads/)), but in the Linux case there could be packages to install, too.

## Linux
One can use the `Makefile` to build the Program:

```
make build
```
and then use it under the `lsas_build` directory.

The current `Makefile` is tested only under Debian 13.

## Windows

Here one can just execute the provided `build.bat`. Then the build program should be in the directory `lsas_build` aswell.

The current `build.bat` ist tested only under Windows 10.

