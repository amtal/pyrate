"""Inline arbitrary x86 assembler inside Python. Pure Python implementation.

This has the potential to become unmanageable fast. I don't want to move to a
3rd party library since staying with the stdlib adds to the challenge and is in
the spirit of the project. However, if the ability to do this is as important
as I think it is, I'll need to figure out a better method than defining a bunch
of constants...

If not a full on on-load assembler, then maybe at least a dictionary-based LUT?
Would be nice to do as much work as possible at module load.
Also, namespace pollution via * import sucks: look for ways to reduce.
Need to further experiment before I can accurately describe requirements...
"""
from ctypes import *
import struct

MOV_EAX_='\xB8';MOV_EBX_='\xBB';MOV_ECX_='\xB9';MOV_EDX_='\xBA' # +DWORD
PUSH_EAX='\x50';PUSH_EBX='\x53';PUSH_ECX='\x51';PUSH_EDX='\x52'
POP_EAX='\x58';POP_EBX='\x5B';POP_ECX='\x59';POP_EDX='\x5A';
CALL_='\xE8'; # +DWORD, relative
CALL_EAX='\xFF\xD0';CALL_EBX='\xFF\xD3' # near
CALL_ECX='\xFF\xD1';CALL_EDX='\xFF\xD2' # near
RETN  = '\xC3'
RETN_ = '\xC2' # +WORD
def DWORD(n): return struct.pack("I", n)
def WORD(n): return struct.pack("H", n)
def asm(code):
    """Unsafely execute arbitrary code.

    Wraps a bunch of arbitrary code as an argless stdcall function.
    Returns a function, which returns a c_uint when called.
    (The retval comes from eax in stdcall, so is totally optional.)
    """
    # get a pointer to the code (and hope page is executable)
    ptr = pointer(c_char_p(code))
    # typecast said pointer as an argless func
    fun = cast(ptr, POINTER(WINFUNCTYPE(c_uint))).contents
    # since there's a call, the code must end with a retn
    # (so the asm isn't embedded so much as called, meh)
    return fun

