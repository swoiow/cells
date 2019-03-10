"""
https://stackoverflow.com/questions/1422368/fcntl-substitute-on-windows

>> for i in dir(fcntl): print(i, getattr(fcntl, i))
"""

import logging


logging.warning("hooking fcntl.py for development/testing purposes only in windows")

DN_ACCESS = 1
DN_ATTRIB = 32
DN_CREATE = 4
DN_DELETE = 8
DN_MODIFY = 2
DN_MULTISHOT = 2147483648
DN_RENAME = 16
FASYNC = 8192
FD_CLOEXEC = 1
F_DUPFD = 0
F_EXLCK = 4
F_GETFD = 1
F_GETFL = 3
F_GETLEASE = 1025
F_GETLK = 5
F_GETLK64 = 5
F_GETOWN = 9
F_GETSIG = 11
F_NOTIFY = 1026
F_RDLCK = 0
F_SETFD = 2
F_SETFL = 4
F_SETLEASE = 1024
F_SETLK = 6
F_SETLK64 = 6
F_SETLKW = 7
F_SETLKW64 = 7
F_SETOWN = 8
F_SETSIG = 10
F_SHLCK = 8
F_UNLCK = 2
F_WRLCK = 1
LOCK_EX = 2
LOCK_MAND = 32
LOCK_NB = 4
LOCK_READ = 64
LOCK_RW = 192
LOCK_SH = 1
LOCK_UN = 8
LOCK_WRITE = 128


def fcntl(fd, op, arg=0):
    return 0


def ioctl(fd, op, arg=0, mutable_flag=True):
    if mutable_flag:
        return 0
    else:
        return ""


def flock(fd, op):
    return


def lockf(fd, operation, length=0, start=0, whence=0):
    return
