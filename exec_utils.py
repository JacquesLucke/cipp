import array
import resource
from ctypes import (
    cdll, memmove, pointer, POINTER,
    c_int, c_long, c_size_t, c_void_p
) 

def createFunctionFromHex(functype, hexCode):
    return createFunctionFromBytes(bytearray.fromhex(hexCode), functype)

def createFunctionFromBytes(data, functype):
    buffer = executableBufferFromBytes(data)
    return functype(buffer)

def executableBufferFromBytes(data):
    arr = array.array("B", data)
    buffer = allocateExecutableMemory(len(arr))
    memmove(buffer, arr.buffer_info()[0], len(arr))
    return buffer

def allocateExecutableMemory(size):
    PROT_READ = 1
    PROT_WRITE = 2
    PROT_EXEC = 4
    buffer = allocatePageAlignedMemory(size)
    mprotect(buffer, size, PROT_READ | PROT_WRITE | PROT_EXEC)
    return buffer

def allocatePageAlignedMemory(size):
    pagesize = resource.getpagesize()
    buffer = c_void_p()
    posix_memalign(pointer(buffer), pagesize, size)
    return buffer.value


libc = cdll.LoadLibrary("libc.so.6")

sysconf = libc.sysconf
sysconf.argtypes = [c_int]
sysconf.restype = c_long

memalign = libc.memalign
memalign.argtypes = [c_size_t, c_size_t]
memalign.restype = c_void_p

mprotect = libc.mprotect
mprotect.argtypes = [c_void_p, c_size_t, c_int]
mprotect.restype = c_int

posix_memalign = libc.posix_memalign
posix_memalign.argtypes = [POINTER(c_void_p), c_size_t, c_size_t]
posix_memalign.restype = c_int