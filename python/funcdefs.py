from ctypes import * # this clutters the namespace of any module that imports *
                     # from funcdefs... but they probably want to import * from
                     # ctypes anyway, so not a big deal
from ezasm import * # more namespace pollution
                    # todo: solve this later

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

# decorator for neatly defining functions
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
    # asm wrapper to load reg+stack according to call conventions
    def cfun(*args):
        # hammer the arguments into c_types if they aren't already
        conv_args = ()
        for arg,arg_t in zip(args,arg_ts):
            if not type(arg)==arg_t:
                conv_args+=(arg_t(arg),)
            else:
                conv_args+=(arg,)
        args = conv_args
        code = ''
        stack_junk = 0
        # EAX, ECX, EDX are available for use in an stdcall, but EBX isn't
        # save EBX and restore it later
        code += PUSH_EBX
        # push arguments to stack, right to left, except 1st and 2nd
        if len(args)>2:
            stack_junk += 4*(len(args)-2) # make sure to pop stack later
            for arg in reversed(args[2:]):
                code += MOV_EAX_+DWORD(arg.value) + PUSH_EAX
        # second arg to EDX
        if len(args)>1: code += MOV_EDX_+DWORD(args[1].value)
        # first arg to ECX
        if len(arg_ts)>0: code += MOV_ECX_+DWORD(args[0].value)
        # call C function we're wrapping with asm
        code += (MOV_EBX_+DWORD(addr)+
                 CALL_EBX)
        # clean stack and restore registers
        code += POP_EBX+RETN_+WORD(stack_junk)
        # call intended function
        ret = c_uint(asm(code)())
        # hammer the retval into a correct shape and return it
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



