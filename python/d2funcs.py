from d2structs import *
from funcdefs import *

# simple function that doesn't require any special work
@stdcall(offset("d2client.dll", 0x41930), c_byte)
def getDifficulty():
    "Returns 0 (Normal) 1 (Nightmare) or 3 (Hell) depending on game difficulty."
    yield (yield ())

# more complex function that mucks with the return value
@stdcall(offset("d2client.dll", 0x108B0), P(GameInfo))
def getGameInfo():
    "Returns a GameInfo structure, used to hold useful multiplayer data."
    ret = yield ()
    if not ret: raise RuntimeError("not in game") # TODO custom exception?
    yield ret.contents

# same as above, but mucks with arguments, not the return value
@stdcall(ordinal("d2common.dll",10304), P(UnitAny), P(Inventory))
def getInvItem(inv):
    "I don't even know. First item in the inventory? No idea."
    if inv==0: raise RuntimeError("null inventory pointer")
    yield (yield inv)

@stdcall(ordinal("d2gfx.dll", 10010), None,
         c_int, c_int, c_int, c_int, c_uint, c_uint)
def drawLine(p1, p2, color):
    (x1,y1),(x2,y2) = p1,p2
    yield (yield x1,y1,x2,y2,color,0)
    
@stdcall(ordinal("d2gfx.dll", 10014), None,
         c_int, c_int, c_int, c_int, c_uint, c_uint)
def drawRect(p1, p2, color, trans):
    (x1,y1),(x2,y2) = p1,p2
    yield (yield x1,y1,x2,y2,color,trans)

@stdcall(ordinal("d2net.dll", 10024), None, c_uint, c_uint, c_char_p)
def sendPacket(data):
    yield (yield len(data),0,data) # is the second parameter 0, or packet id?
                                   # possible TODO, debug

# oh crud how do I -neatly- deal with mutable pass-by-ref?
@stdcall(ordinal("d2common.dll", 11087), None, P(c_uint), P(c_uint))
def map2screen(x,y):
    "Turn map coordinates into window/mouse coordinates."
    # don't have access to modified pointers due to @stdcall abstraction...
    yield (yield x,y))
@stdcall(ordinal("d2common.dll", 10474), None, P(c_uint), P(c_uint))
def screen2map(x,y):
    "Vice versa."
    yield (yield x,y))





