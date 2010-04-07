from d2structs import *
from funcdefs import *

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

# some variables (d2client.dll stuff only works in-game)
playerUnit = varptr(UnitAny, offset("d2client.dll", 0x11BBFC))
mouseX =     varptr(c_uint,  offset("d2client.dll", 0x11B828)).value
mouseY =     varptr(c_uint,  offset("d2client.dll", 0x11B824)).value
