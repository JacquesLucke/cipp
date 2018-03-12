import sys
import array
from ctypes import (
    cdll, memmove, pointer, POINTER,
    c_int, c_long, c_size_t, c_void_p, c_uint32
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

    def allocateExecutableMemory(size):
        PROT_READ = 1
        PROT_WRITE = 2
        PROT_EXEC = 4
        buffer = allocatePageAlignedMemory(size)
        mprotect(buffer, size, PROT_READ | PROT_WRITE | PROT_EXEC)
        return buffer

    def allocatePageAlignedMemory(size):
        import resource
        pagesize = resource.getpagesize()
        buffer = c_void_p()
        posix_memalign(pointer(buffer), pagesize, size)
        return buffer.value

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