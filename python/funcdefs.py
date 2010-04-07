from ctypes import * # this clutters the namespace of any module that imports *
                     # from funcdefs... but they probably want to import * from
                     # ctypes anyway, probably won't be a big deal

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
# deuglification synonym
P = POINTER

# decorator for neatly defining functions
def stdcall(addr, ret_t, *arg_ts):
    # prebuild C type sig, and instantiate with address, at module load time
    cfun = WINFUNCTYPE(ret_t, *arg_ts)(addr)
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

# quick variable pointer definition
def varptr(ret_t, addr):
    return cast(addr, P(ret_t)).contents



