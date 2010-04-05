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

def getInvItem(inv):
    if inv==0: raise RuntimeError("null inventory pointer")
    decl = WINFUNCTYPE(POINTER(UnitAny), POINTER(Inventory))
    defn = decl(ordinal("d2common.dll",10304))
    return defn(inv).contents

def getGameInfo():
    f = WINFUNCTYPE(POINTER(GameInfo))(base["d2client.dll"]+0x108B0)
    return f().contents

#getGameInfo = stdcall(POINTER(GameInfo),offset("d2client.dll",0x108B0))


                  
getDifficulty = WINFUNCTYPE(c_byte)(base["d2client.dll"]+0x41930)

playerUnit = cast(get_dlls()["d2client.dll"]+0x11BBFC, POINTER(UnitAny))
mouseX = cast(base["d2client.dll"]+0x11B828, POINTER(c_uint)).contents
mouseY = cast(base["d2client.dll"]+0x11B824, POINTER(c_uint)).contents
