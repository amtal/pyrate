"""Inline arbitrary x86 assembler inside Python. Pure Python implementation.

Uses a subset of the Intel syntax. Only important instructions implemented.
Instructions separated by newlines or semicolons. No comments.
Code can be specialized during:
    ASSEMBLY: by using $named_tags, then passing named values to assemble()
    EXECUTION: by using Python {str.format} tags, which will be inserted into
        machine code and can be str.formatted at a later time.
"""
import struct
import ctypes as ct

def DWORD(n): return struct.pack("I", n)
def WORD(n): return struct.pack("H", n)

_opcodes = {
    'mov':{ # +DWORD
        'eax':{'$':'\xB8'},
        'ecx':{'$':'\xB9'},
        'edx':{'$':'\xBA'},
        'ebx':{'$':'\xBB'},
        },
    'push':{
        'eax':'\x50',
        'ecx':'\x51',
        'edx':'\x52',
        'ebx':'\x53'
        },
    'pop':{
        'eax':'\x58',
        'ecx':'\x59',
        'edx':'\x5A',
        'ebx':'\x5B'
        },
    'call':{
        # near
        'eax':'\xFF\xD0',
        'ecx':'\xFF\xD1',
        'edx':'\xFF\xD2',
        'ebx':'\xFF\xD3',
        # +DWORD, relative
        '$':'\xE8'
        },
    'retn':{
        None:'\xC3',
        '$':'\xC2'
        }
    }
# { and } are 7B and 7D... $ is 0x24

def prettify(asm):
    """Normalizes semicolons to newlines, and removes excess whitespace."""
    return '\n'.join(map(str.strip, asm.replace(';','\n').split('\n')))
    
def assemble(asm, **args):
    # process to consistent format
    asm = prettify(asm)
    # assemble line by line, token by token
    code = ''
    for line in asm.split('\n'):
        # each line is a separate, single instruction
        if line.strip()=='': continue
        lup = _opcodes
        const = '' # assume: only one constant per instruction?
        for tok in line.split():
            # step down the syntax tree:
            #   -finding the instruction encoding
            #   -identifying the constant, if it exists
            lup_id = tok
            if tok[0]=='$':
                lup_id,const='$',args[tok[1:]]
            elif tok[0]=='{':
                lup_id,const='$',tok
            if not lup_id in lup:
                raise RuntimeError('asm syntax lup failure:',lup_id,'in',lup)
            lup = lup[lup_id]
        # have we reached the data part yet?
        if type(lup) is dict:
            # early termination of instruction, eg argless retn
            lup = lup[None]
        if type(lup) is str:
            # instruction encoding reached
            #print 'Encoding "{0}" as "{1}" + "{2}"'.format(line,lup,const)
            code += lup+const
        else:
            raise RuntimeError('Opcode lup did not terminate:',lup)
    return code
            
def call(code):
    """Unsafely execute arbitrary machine code.

    Wraps a bunch of arbitrary code as an argless stdcall function.
    Returns a function, which returns a c_uint when called.
    (The retval comes from eax in stdcall, so is totally optional.)
    """
    # get a pointer to the code (and hope page is executable)
    ptr = ct.pointer(ct.c_char_p(code))
    # typecast said pointer as an argless func
    fun = ct.cast(ptr, ct.POINTER(ct.WINFUNCTYPE(ct.c_uint))).contents
    # since there's a call, the code must end with a retn
    # (so the asm isn't embedded so much as called, meh)
    return fun
