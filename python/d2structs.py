from ctypes import *

class GameInfo(Structure):
    _fields_ = [
        ("_1",      c_uint*6),
        ("_2",      c_ushort),
        ("name",    c_char*0x18),
        ("ip",      c_char*0x56), # only name seems to be read correctly
        ("account", c_char*0x30), # bug?
        ("char",    c_char*0x18),
        ("realm",   c_char*0x18),
        ("_2",      c_byte*0x158), # d2bs has WAY more detailed version of this
        ("password",c_char*0x18)
    ]

# Forward declarations of non-trivial structures containing pointers to
# themselves or other structures.

class Inventory(Structure):
    pass
class UnitAny(Structure):
    pass

# Field definitions for non-trivial structures.

UnitAny._fields_ = [
    ("unitType",    c_uint),
    ("txtFileNo",   c_uint),
    ("_1",          c_uint),
    ("unitId",      c_uint),
    ("mode",        c_uint),
    ("unitData",    POINTER(c_uint)),
    ("act",         c_uint),
    ("actP",        POINTER(c_int)),
    ("seed",        c_uint*2),
    ("_2",          c_int),
    ("path",        POINTER(c_uint)),
    ("_3",          c_uint*5),
    ("gfxFrame",    c_int),
    ("frameRemain", c_int),
    ("frameRate",   c_ushort),
    ("_4",          c_int),
    ("pGfxUnk",     POINTER(c_byte)),
    ("pGfxInfo",    POINTER(c_uint)),
    ("_5",          c_uint),
    ("statList",    POINTER(c_int)),
    ("inventory",   POINTER(Inventory)),
    ("light",       POINTER(c_int)),
    ("_6",          c_uint*9),
    ("X",           c_ushort),
    ("Y",           c_ushort),
    ("_7",          c_uint),
    ("ownerType",   c_uint),
    ("ownerId",     c_uint),
    ("_8",          c_uint*2),
    ("overheadMsg", POINTER(c_int)),
    ("info",        POINTER(c_int)),
    ("_9",          c_uint*6),
    ("flags",       c_uint),
    ("flags2",      c_uint),
    ("_10",         c_uint*5),
    ("changedNext", POINTER(UnitAny)),
    ("roomNext",    POINTER(UnitAny)),
    ("listNext",    POINTER(UnitAny))
]


Inventory._fields_ = [
    ("signature",   c_uint),
    ("game1C",      POINTER(c_byte)),
    ("owner",       POINTER(UnitAny)),
    ("first",       POINTER(UnitAny)),
    ("last",        POINTER(UnitAny)),
    ("_1",          c_uint*2),
    ("leftItemUid", c_uint),
    ("cursorItem",  POINTER(UnitAny)),
    ("ownerId",     c_uint),
    ("itemCount",   c_uint)
]
