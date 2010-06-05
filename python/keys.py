from ctypes import *
from d2funcs import *
import Queue

key_events = Queue.Queue()

def test():
    with open("keys.log", "a") as f:
        f.write("call")
        
def get():
    return key_events.get()
    
def windowProc(hwnd, uMsg, wParam, lParam):
    test()
    if uMsg==WM_KEYDOWN:
        global key_events
        key_events.put((wParam,lParam))
        print 'Keydown:',wParam,lParam
    return windll.User32.CallWindowProcA(oldWindowProc, hwnd, uMsg, wParam,
                                                                   lParam)
def f():
    print oldWindowProc

hWnd = getHWnd()
print 'hWnd acquired:', hWnd

GWLP_WNDPROC = -4 # WinUser.h
WM_KEYDOWN = 0x0100

callback = WINFUNCTYPE(c_uint,
                       c_uint, c_uint, c_int, c_int)(windowProc)
callback = cast(pointer(callback), POINTER(c_int)).contents

print callback

oldWindowProc = windll.user32.SetWindowLongA(hWnd, GWLP_WNDPROC, callback)
print oldWindowProc
