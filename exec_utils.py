import sys
import array
from ctypes import (
    cdll, memmove, pointer, POINTER,
    c_int, c_long, c_size_t, c_void_p, c_uint32,
)

onLinux = sys.platform.startswith("linux")
onWindows = sys.platform.startswith("win")

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

if onLinux:

    libc = cdll.LoadLibrary("libc.so.6")

    mprotect = libc.mprotect
    mprotect.argtypes = [c_void_p, c_size_t, c_int]
    mprotect.restype = c_int

    posix_memalign = libc.posix_memalign
    posix_memalign.argtypes = [POINTER(c_void_p), c_size_t, c_size_t]
    posix_memalign.restype = c_int

    mmap = libc.mmap
    mmap.argtypes = [c_void_p, c_size_t, c_int, c_int, c_int, c_long]
    mmap.restype = c_void_p

    def allocateExecutableMemory(size):
        PROT_READ = 1
        PROT_WRITE = 2
        PROT_EXEC = 4
        MAP_PRIVATE = 2
        MAP_ANONYMOUS = 32
        return mmap(0, 4096, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE | MAP_ANONYMOUS, 0, 0)

elif onWindows:

    from ctypes import windll

    virtualAlloc = windll.kernel32.VirtualAlloc
    virtualAlloc.argtypes = [c_void_p, c_size_t, c_uint32, c_uint32]
    virtualAlloc.restype = c_void_p

    virtualProtect = windll.kernel32.VirtualProtect
    virtualProtect.argtypes = [c_void_p, c_size_t, c_uint32, POINTER(c_uint32)]
    virtualProtect.restype = c_int

    def allocateExecutableMemory(size):
        MEM_COMMIT = 0x1000
        PAGE_READWRITE = 4
        buffer = virtualAlloc(None, size, MEM_COMMIT, PAGE_READWRITE)

        PAGE_EXECUTE_READWRITE = 0x40
        virtualProtect(buffer, size, PAGE_EXECUTE_READWRITE, pointer(c_uint32()))

        return buffer
