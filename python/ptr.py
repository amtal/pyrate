from ctypes import *
from d2structs import *

## HELPER FUNCTIONS (TODO move to separate module)

# base DLL address calculation
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

# address calculation
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
        # intern() "wraps" around f, and gets called every time f is
        def intern(*args):
            # instantiate coroutine generator with the argument list
            gen = f(*args)
            # get the argument list, which coroutine may have modified
            args = gen.send(None)
            # execute c function
            ret = cfun(*args)
            # pass result by f again, in case it should be modified
            ret = gen.send(ret)
            return ret
        return intern
    return wrap

# quickie varpointer definition
def varptr(ret_t, addr):
    return cast(addr, P(ret_t)).contents


## SAMPLE FUNCTIONS

# simple function that doesn't require any special work
@stdcall(offset("d2client.dll", 0x41930), c_byte)
def getDiff(): yield (yield ())

# more complex function that mucks with the return value
@stdcall(offset("d2client.dll", 0x108B0), P(GameInfo))
def getGameInfo():
    ret = yield ()
    if not ret: raise RuntimeError("not in game") # TODO custom exception!
    yield ret.contents

# same as above, but arguments, not the return value
@stdcall(ordinal("d2common.dll",10304), P(UnitAny), P(Inventory))
def getInvItem(inv):
    if inv==0: raise RuntimeError("null inventory pointer")
    yield (yield inv)


# some variables

playerUnit = varptr(UnitAny, offset("d2client.dll", 0x11BBFC))
# only works in-game:
mouseX =     varptr(c_uint,  offset("d2client.dll", 0x11B828))
mouseY =     varptr(c_uint,  offset("d2client.dll", 0x11B824))
