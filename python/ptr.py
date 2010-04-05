from ctypes import *
from d2structs import *

def get_dlls():
    names = "d2client d2common d2gfx d2lang d2win d2net d2game d2launch fog\
             bnclient storm d2cmp d2multi".split()
    addrs = {}
    for name in names:
        name+=".dll"
        hmod = windll.kernel32.LoadLibraryA(name)
        if not hmod: raise RuntimeError("could not load "+name)
        addrs[name]=hmod
    return addrs
base = get_dlls()

def offset(dll_name, dx):
    return base[dll_name]+dx
def ordinal(dll_name, o):
    return windll.kernel32.GetProcAddress(base[dll_name],
                                          cast(o,c_char_p))

# better known, less ugly synonym
# (maybe make it allcaps, since ctypes uses allcaps to define types, and
# this function creates a function type which is instanciated by passing
# it an address?)
STDCALL = WINFUNCTYPE

def getInvItem(inv):
    if inv==0: raise RuntimeError("null inventory pointer")
    ftype = STDCALL(POINTER(UnitAny), POINTER(Inventory))
    finst = ftype(ordinal("d2common.dll",10304))
    return defn(inv).contents

def getGameInfo():
    f = STDCALL(POINTER(GameInfo))(offset("d2client.dll",0x108B0))
    return f().contents

                  
getDifficulty = STDCALL(c_byte)(offset("d2client.dll", 0x41930))

playerUnit = cast(offset("d2client.dll", 0x11BBFC), POINTER(UnitAny))
mouseX = cast(offset("d2client.dll", 0x11B828), POINTER(c_uint)).contents
mouseY = cast(offset("d2client.dll", 0x11B824), POINTER(c_uint)).contents
