from ctypes import * # this clutters the namespace of any module that imports *
                     # from funcdefs... but they probably want to import * from
                     # ctypes anyway, so not a big deal
import asm

# find DLL base addresses
def get_base_addrs():
    names = "d2client d2common d2gfx d2lang d2win d2net d2game d2launch fog\
             bnclient storm d2cmp d2multi".split()
    addrs = {}
    for name in names:
        name+=".dll"
        hmod = windll.kernel32.LoadLibraryA(name)
        if not hmod: raise RuntimeError("could not load "+name)
        addrs[name]=hmod
    return addrs
base = get_base_addrs()

# final address calculations
def offset(dll_name, dx):
    return base[dll_name]+dx
def ordinal(dll_name, o):
    return windll.kernel32.GetProcAddress(base[dll_name],
                                          cast(o,c_char_p))
# deuglification synonyms
P = POINTER
STDCALL = WINFUNCTYPE # types for manually calling functions
CDECL = CFUNCTYPE

# decorators for neatly defining functions
def stdcall(addr, ret_t, *arg_ts):
    """In-process functions with __stdcall calling convention.

    Arguments pushed on stack right-to-left. Callee cleans up stack.
    EAX,ECX,EDX available for use within function. Return in EAX.
    """
    return simple_call(STDCALL, addr, ret_t, *arg_ts)

def cdecl(addr, ret_t, *arg_ts):
    """In-process functions with __cdecl calling convention.

    Arguments pushed on stack right-to-left. Caller cleans up stack.
    EAX,ECX,EDX available for use within function. Return in EAX.
    """
    return simple_call(CDECL, addr, ret_t, *arg_ts)

def simple_call(call_type, addr, ret_t, *arg_ts):
    # prebuild C type sig, and instantiate with address, at module load time
    cfun = call_type(ret_t, *arg_ts)(addr)
    def wrap(f):
        # intern() "wraps" around f, and gets called every time f does
        # f is a coroutine that yields twice:
        #   once to pass on the (potentially modified) arglist
        #   again to pass on the (potentially modified) return value
        def intern(*args):
            gen = f(*args)
            args = gen.send(None) # let coroutine work with args if it wants to
            ret = cfun(*args) # execute C function, hope it doesn't failboat
            ret = gen.send(ret) # let coroutine work with retval if it wants to
            return ret
        return intern
    return wrap


# the MS fastcall convention isn't directly supported, so tricks are required...
def fastcall(addr, ret_t, *arg_ts):
    """In-process functions with MS __fastcall calling convention.

    First two arguments passed in ECX and EDX, left-to-right.
    The rest are pushed on stack right-to-left. Callee cleans up stack.
    Return in EAX. (EAX,ECX,EDX are thus available for use.)
    """
    # assemble an asm wrapper around the function
    # this gets done just once, at module load time, by the decorator
    #
    # since parameters are unknown, the machine code is parametrized via
    # string.format(*args), to be swapped in on function call
    #
    # alternatively, could wrap with an stdcall... but eh, this is more flexible
    s = 'push ebx;'
    junk = 0 # how many bytes to clean off the stack
    # first two arguments in registers
    if len(arg_ts)>0: s += 'mov ecx {0};'
    if len(arg_ts)>1: s += 'mov edx {1};'
    # variable arguments on the stack
    vargs = len(arg_ts)-2
    if vargs>0:
        junk += 4*vargs # args are DWORDs
        for n in range(2, 2+vargs):
            s += 'mov eax {%d}; push eax;' % (n,)
    # function call and cleanup
    s +='''
        mov ebx $func_addr
        call ebx
        pop ebx
        retn $stack_junk
        '''
    asm_code = s
    machine_code = asm.assemble(asm_code,
                                func_addr=asm.DWORD(addr),
                                stack_junk=asm.WORD(junk))
    
    def cfun(*args):
        # pack arguments into 4-byte form suitable for stack
        # TODO sign?
        # TODO proper handling of arg_ts ctypes
        conv_args = ()
        for arg in args:
                conv_args+=(asm.DWORD(arg),)
        args = conv_args
        # insert particular arguments into preassembled machine code
        code = machine_code.format(*args)
        # execute
        ret = c_uint(asm.call(code)())
        # hammer the retval into a correct shape via pointer typecast
        return cast(pointer(ret), POINTER(ret_t)).contents
    
    def wrap1(f):
        # this part is just like it was for stdcall and cdecl
        def wrap2(*args):
            gen = f(*args)
            args = gen.send(None) # let coroutine work with args if it wants to
            ret = cfun(*args) # execute C function, hope it doesn't failboat
            ret = gen.send(ret) # let coroutine work with retval if it wants to
            return ret
        return wrap2
    return wrap1


# quick variable pointer definition
def varptr(ret_t, addr):
    '''Pointer to a variable.

    Can be read via .contents, or read+modified via [0].
    [1], [2], [...] does the intuitive thing.
    '''
    return cast(addr, P(ret_t))



