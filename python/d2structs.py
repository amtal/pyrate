from ctypes import *

# 1.13c
class OverheadMsg(Structure):
    _fields_ = [
        ("_1",          c_uint),
        ("trigger",     c_uint),
        ("_2",          c_uint*2),
        ("msg",         c_char*232)
    ]

# 1.13c
class InventoryInfo(Structure):
    _fields_ = [
        ("location",    c_int),
        ("maxXCells",   c_int),
        ("maxYCells",   c_int)
    ]

# 1.13c
class GfxCell(Structure):
    _fields_ = [
        ("flags",       c_uint),
        ("width",       c_uint),
        ("height",      c_uint),
        ("xOffset",     c_uint),
        ("yOffset",     c_uint),
        ("_1",          c_uint),
        ("pParent",     c_uint),
        ("cols",        c_byte)
    ]
    
# 1.13c
class GameInfo(Structure):
    _fields_ = [
        ("_1",          c_byte*0x1B),
        ("name",        c_char*0x18),
        ("ip",          c_char*0x56),
        ("account",     c_char*0x30), 
        ("char",        c_char*0x18),
        ("realm",       c_char*0x18),
        ("_2",          c_byte*0x158),
        ("password",    c_char*0x18)
    ]

# 1.13c
class Stat(Structure):
    _fields_ = [
        ("subIndex",    c_ushort),
        ("statIndex",   c_ushort),
        ("statValue",   c_uint)
    ]

class _ItemCode(Union):
    _fields_ = [
        ("code",        c_uint),
        ("sCode",       c_char*4),
        ]
    
class _UnitPath(Union):
    pass
class _UnitData(Union):
    pass
    
# Forward declarations of non-trivial structures containing pointers to
# themselves or other structures.

class AutomapLayer(Structure):
    pass
class AutomapLayer2(Structure):
    pass
class InteractStruct(Structure):
    pass
class AutomapCell(Structure):
    pass
class Inventory(Structure):
    pass
class UnitAny(Structure):
    pass
class PlayerData(Structure):
    pass
class ItemData(Structure):
    pass
class MonsterData(Structure):
    pass
class ObjectData(Structure):
    pass
class InventoryLayout(Structure):
    pass
class ItemTxt(Structure):
    pass
class ControlText(Structure):
    pass
class StatList(Structure):
    pass
class Path(Structure):
    pass
class ItemPath(Structure):
    pass
class ObjectPath(Structure):
    pass
class Room1(Structure):
    pass
class Room2(Structure):
    pass
class Level(Structure):
    pass
class PresetUnit(Structure):
    pass
class CollMap(Structure):
    pass
class RoomTile(Structure):
    pass
class Act(Structure):
    pass
class ActMisc(Structure):
    pass
class SkillInfo(Structure):
    pass
class Skill(Structure):
    pass
class Info(Structure):
    pass
class CellContext(Structure):
    pass
class CellFile(Structure):
    pass

# Field definitions for non-trivial structures (structs with pointers in them)

# 1.13c
AutomapCell._fields_ = [
    ("fSaved",      c_uint),
    ("nCellNo",     c_ushort),
    ("xPixel",      c_ushort),
    ("yPixel",      c_ushort),
    ("wWeight",     c_ushort),
    ("pLess",       POINTER(AutomapCell)),
    ("pMore",       POINTER(AutomapCell))
    ]

# 1.13c
AutomapLayer._fields_ = [
    ("layerNo",     c_uint),
    ("fSaved",      c_uint),
    ("pFloors",     POINTER(AutomapCell)),
    ("pWalls",      POINTER(AutomapCell)),
    ("pObjects",    POINTER(AutomapCell)),
    ("pExtras",     POINTER(AutomapCell)),
    ("pNextLayer",  POINTER(AutomapLayer))
    ]

# 1.13c
AutomapLayer2._fields_ = [
    ("_1",          c_uint*2),
    ("layerNo",     c_uint)
    ]

# 1.13c
CellFile._fields_ = [
    ("version",     c_uint),
    ("flags",       c_uint), # FIXME: written as a struct in D2Structs.h
    ("eFormat",     c_uint),
    ("termination", c_uint),
    ("numdirs",     c_uint),
    ("numcells",    c_uint),
    ("cells",       POINTER(GfxCell))
    ]

# 1.13c
CellContext._fields_ = [
    ("_1",          c_uint*13),
    ("pCellFile",   POINTER(CellFile)),
    ("_2",          c_uint*4)
    ]

#1.13c
Path._fields_ = [
    ("xOffset",     c_ushort),
    ("xPos",        c_ushort),
    ("yOffset",     c_ushort),
    ("yPos",        c_ushort),
    ("_1",          c_uint*2),
    ("xTarget",     c_ushort),
    ("yTarget",     c_ushort),
    ("_2",          c_uint*2),
    ("pRoom1",      POINTER(Room1)),
    ("pRoomUnk",    POINTER(Room1)),
    ("_3",          c_uint*3),
    ("pUnit",       POINTER(UnitAny)),
    ("flags",       c_uint),
    ("_4",          c_uint),
    ("pathType",    c_uint),
    ("prevPathType",c_uint),
    ("unitSize",    c_uint),
    ("_5",          c_uint*4),
    ("pTargetUnit", POINTER(UnitAny)),
    ("targetType",  c_uint),
    ("targetId",    c_uint),
    ("direction",   c_byte)
    ]

# 1.13c (unverified)
ItemPath._fields_ = [
    ("_1",          c_uint*3),
    ("xPos",        c_uint),
    ("yPos",        c_uint),
    # rest is copied from Path
    ("xTarget",     c_ushort),
    ("yTarget",     c_ushort),
    ("_2",          c_uint*2),
    ("pRoom1",      POINTER(Room1)),
    ("pRoomU",      POINTER(Room1)),
    ("_3",          c_uint*3),
    ("pUnit",       POINTER(UnitAny)),
    ("flags",       c_uint),
    ("_4",          c_uint),
    ("pathType",    c_uint),
    ("prevPathType",c_uint),
    ("unitSize",    c_uint),
    ("_5",          c_uint*4),
    ("pTargetUnit", POINTER(UnitAny)),
    ("targetType",  c_uint),
    ("targetId",    c_uint),
    ("direction",   c_byte)
    ]

# 1.13c (unverified)
ObjectPath._fields_ = [
    ("pRoom1",      POINTER(Room1)),
    ("_1",          c_uint*2),
    ("xPos",        c_uint),
    ("yPos",        c_uint),
    # rest copied from Path
    ("xTarget",     c_ushort),
    ("yTarget",     c_ushort),
    ("_2",          c_uint*2),
    ("pRoom1",      POINTER(Room1)),
    ("pRoomU",      POINTER(Room1)),
    ("_3",          c_uint*3),
    ("pUnit",       POINTER(UnitAny)),
    ("flags",       c_uint),
    ("_4",          c_uint),
    ("pathType",    c_uint),
    ("prevPathType",c_uint),
    ("unitSize",    c_uint),
    ("_5",          c_uint*4),
    ("pTargetUnit", POINTER(UnitAny)),
    ("targetType",  c_uint),
    ("targetId",    c_uint),
    ("direction",   c_byte)
    ]

_UnitPath._fields_ = [
    ("pPath",       POINTER(Path)),
    ("pItemPath",   POINTER(ItemPath)),
    ("pObjectPath", POINTER(ObjectPath))
    ]

ItemData._fields_ = [
    ("quality",     c_uint),
    ("_1",          c_uint*2),
    ("itemFlags",   c_uint),
    ("_2",          c_uint*2),
    ("flags",       c_uint),
    ("_3",          c_uint*3),
    ("quality2",    c_uint),
    ("itemLevel",   c_uint),
    ("_4",          c_uint*2),
    ("prefix",      c_ushort),
    ("_5",          c_ushort*2),
    ("suffix",      c_ushort),
    ("_6",          c_uint),
    ("bodyLocation",c_byte),
    ("itemLocation",c_byte),
    ("_7",          c_byte),
    ("_8",          c_ushort),
    ("_9",          c_uint*4),
    ("pOwnerInventory",POINTER(Inventory)),
    ("_10",         c_uint),
    ("pNextInvItem", POINTER(UnitAny)),
    ("_11",         c_byte),
    ("nodePage",    c_byte),
    ("_12",         c_ushort),
    ("_13",         c_uint*6),
    ("pOwner",      POINTER(UnitAny))
    ]

_UnitData._fields_ = [
    ("pPlayerData", POINTER(PlayerData)),
    ("pItemData",   POINTER(ItemData)),
    ("pMonsterData",POINTER(MonsterData)),
    ("pObjectData", POINTER(ObjectData))
    ]

UnitAny._anonymous_ = ("pUnitData","pPath",)
UnitAny._fields_ = [
    ("unitType",    c_uint),
    ("txtFileNo",   c_uint),
    ("_1",          c_uint),
    ("unitId",      c_uint),
    ("mode",        c_uint),
    ("pUnitData",   _UnitData),
    ("act",         c_uint),
    ("pAct",        POINTER(Act)),
    ("seed",        c_uint*2),
    ("_2",          c_int),
    ("pPath",       _UnitPath),
    ("_3",          c_uint*5),
    ("gfxFrame",    c_int),
    ("frameRemain", c_int),
    ("frameRate",   c_ushort),
    ("_4",          c_ushort),
    ("pGfxUnk",     POINTER(c_byte)),
    ("pGfxInfo",    POINTER(c_uint)),
    ("_5",          c_uint),
    ("pStatList",   POINTER(StatList)),
    ("pInventory",  POINTER(Inventory)),
    ("pLight",      POINTER(c_int)),
    ("_6",          c_uint*9),
    ("X",           c_ushort),
    ("Y",           c_ushort),
    ("_7",          c_uint),
    ("ownerType",   c_uint),
    ("ownerId",     c_uint),
    ("_8",          c_uint*2),
    ("pOverheadMsg",POINTER(c_int)),
    ("pInfo",       POINTER(Info)),
    ("_9",          c_uint*6),
    ("flags",       c_uint),
    ("flags2",      c_uint),
    ("_10",         c_uint*5),
    ("pChangedNext",POINTER(UnitAny)),
    ("pRoomNext",   POINTER(UnitAny)),
    ("pListNext",   POINTER(UnitAny))
]

InteractStruct._fields_ = [
    ("moveType",    c_uint),
    ("pPlayerUnit", POINTER(UnitAny)),
    ("pTargetUnit", POINTER(UnitAny)),
    ("targetX",     c_uint),
    ("targetY",     c_uint),
    ("_1",          c_uint),
    ("_2",          c_uint)
    ]

Inventory._fields_ = [
    ("signature",   c_uint),
    ("pGame1C",     POINTER(c_byte)),
    ("pOwner",      POINTER(UnitAny)),
    ("pFirst",      POINTER(UnitAny)),
    ("pLast",       POINTER(UnitAny)),
    ("_1",          c_uint*2),
    ("leftItemUid", c_uint),
    ("pCursorItem", POINTER(UnitAny)),
    ("ownerId",     c_uint),
    ("itemCount",   c_uint)
]

InventoryLayout._fields_ = [
    ("slotWidth",   c_byte),
    ("slotHeight",  c_byte),
    ("_1",          c_byte),
    ("_2",          c_byte),
    ("left",        c_uint),
    ("right",       c_uint),
    ("top",         c_uint),
    ("bottom",      c_uint),
    ("slotPixelWidth",  c_byte),
    ("slotPixelHeight", c_byte)
    ]

ItemTxt._anonymous_ = ("code",)
ItemTxt._fields_ = [
    ("Name2",       c_wchar*0x40),
    ("code",        _ItemCode),
    ("_2",          c_byte*0x70),
    ("nLocaleTxtNo",c_ushort),
    ("_2a",         c_byte*0x19),
    ("xSize",       c_byte),
    ("ySize",       c_byte),
    ("_2b",         c_byte*13),
    ("nType",       c_byte),
    ("_3",          c_byte*0xd),
    ("fQuest",      c_byte)
    ]

ControlText._fields_ = [
    ("wText",       c_wchar_p),
    ("wText2",      c_wchar_p),
    ("_1",          c_uint*3),
    ("color",       c_uint),
    ("_2",          c_uint),
    ("pNext",       POINTER(ControlText))
    ]

StatList._fields_ = [
    ("_1",          c_uint),
    ("pUnit",       POINTER(UnitAny)),
    ("unitType",    c_uint),
    ("unitId",      c_uint),
    ("flags",       c_uint),
    ("_2",          c_uint*4),
    ("pStat",       POINTER(Stat)),
    ("count",       c_ushort),
    ("nSize",       c_ushort),
    ("pPrevLink",   POINTER(StatList)),
    ("_3",          c_uint),
    ("pPrev",       POINTER(StatList)),
    ("_4",             POINTER(c_byte)),
    ("pNext",       POINTER(StatList)),
    ("pSetList",    POINTER(StatList)),
    ("_5",          c_uint),
    ("pSetStat",    POINTER(Stat)),
    ("setStatCount",c_short)
    ]

# 1.13c
Room1._fields_ = [
    ("ppRoomsNear", POINTER(POINTER(Room1))),
    ("_1",          c_uint*3),
    ("pRoom2",      POINTER(Room2)),
    ("_2",          c_uint*3),
    ("coll",        POINTER(CollMap)),
    ("roomsNear",   c_uint),
    ("_3",          c_uint*9),
    ("xPos",        c_uint),
    ("yPos",        c_uint),
    ("xSize",       c_uint),
    ("ySize",       c_uint),
    ("_4",          c_uint*6),
    ("pUnitFirst",  POINTER(UnitAny)),
    ("_5",          c_uint),
    ("pRoomNext",   POINTER(Room1))
    ]

# 1.13c
Room2._fields_ = [
    ("_1",          c_uint*2),
    ("pRoom2Near",  POINTER(Room2)),
    ("_2",          c_uint*6),
    ("pRoom2Next",  POINTER(Room2)),
    ("roomFlags",   c_uint),
    ("roomsNear",   c_uint),
    ("pRoom1",      POINTER(Room1)),
    ("xPos",        c_uint),
    ("yPos",        c_uint),
    ("xSize",       c_uint),
    ("ySize",       c_uint),
    ("_3",          c_uint),
    ("presetType",  c_uint),
    ("pRoomTiles",  POINTER(RoomTile)),
    ("_4",          c_uint*2),
    ("pLevel",      POINTER(Level)),
    ("pPreset",     POINTER(PresetUnit))
    ]

# 1.13c
Level._fields_ = [
    ("_1",          c_uint*4),
    ("pRoom2First", POINTER(Room2)),
    ("_2",          c_uint*2),
    ("xPos",        c_uint),
    ("yPos",        c_uint),
    ("xSize",       c_uint),
    ("ySize",       c_uint),
    ("_3",          c_uint*96),
    ("pNextLevel",  POINTER(Level)),
    ("_4",          c_uint),
    ("pMisc",       POINTER(ActMisc)),
    ("_5",          c_uint*3),
    ("seed",        c_uint*2),
    ("_6",          c_uint),
    ("levelNo",     c_uint)
    ]

# 1.13c
ActMisc._fields_ = [
    ("_1",          c_uint*37),
    ("staffTombLevel",  c_uint),
    ("_2",          c_uint*245),
    ("pAct",        POINTER(Act)),
    ("_3",          c_uint*3),
    ("pLevelFirst", POINTER(Level))
    ]

# 1.13c
Act._fields_ = [
    ("_1",          c_uint*3),
    ("mapSeed",     c_uint),
    ("pRoom1",      POINTER(Room1)),
    ("act",         c_uint),
    ("_2",          c_uint*12),
    ("pMisc",       POINTER(ActMisc)),
    ]

# 1.13c
PresetUnit._fields_ = [
    ("_1",          c_uint),
    ("txtFileNo",   c_uint),
    ("xPos",        c_uint),
    ("pPresetNext", POINTER(PresetUnit)),
    ("_2",          c_uint),
    ("type",        c_uint),
    ("yPos",        c_uint)
    ]

# 1.13c
SkillInfo._fields_ = [
    ("skillId",     c_ushort)
    ]

# 1.13c
Skill._fields_ = [
    ("pSkillInfo",  POINTER(SkillInfo)),
    ("pNextSkill",  POINTER(Skill)),
    ("_1",          c_uint*8),
    ("skillLevel",  c_uint),
    ("_2",          c_uint),
    ("flags",       c_uint)
    ]

# 1.13c
Info._fields_ = [
    ("pGame1C",     POINTER(c_byte)),
    ("pFirstSkill", POINTER(Skill)),
    ("pLeftSkill",  POINTER(Skill)),
    ("pRightSkill", POINTER(Skill))
    ]
