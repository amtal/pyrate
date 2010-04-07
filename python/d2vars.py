from d2structs import *
from funcdefs import *

# some variables (these can be read, but I haven't got writing to work yet)
playerUnit = varptr(UnitAny, offset("d2client.dll", 0x11BBFC))
selectedUnit = varptr(UnitAny, offset("d2client.dll", 0x11C4D8))
mouse      = (varptr(c_uint,  offset("d2client.dll", 0x11B828)),
              varptr(c_uint,  offset("d2client.dll", 0x11B824)))
screenSize = (varptr(c_uint,  offset("d2client.dll", 0xDBC48)),
              varptr(c_uint,  offset("d2client.dll", 0xDBC4C)))
ping       = varptr(c_uint,  offset("d2client.dll", 0x119804))
skip       = varptr(c_uint,  offset("d2client.dll", 0x119810))
fps        = varptr(c_uint,  offset("d2client.dll", 0x11C2AC))
automapOn  = varptr(c_uint,  offset("d2client.dll", 0xFADA8))
serverIP  = varptr(c_char*13,  offset("d2client.dll", 0xF4320))
