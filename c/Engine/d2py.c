#include <windows.h>
#include <stdio.h>
#include "main.h"

// Was used for MessageBox when stdout wasn't enough:
//#pragma comment(lib, "User32")

HANDLE hThread;
DWORD threadId;

BOOL WINAPI DllMain(__in HINSTANCE hinstDLL, __in DWORD fdwReason, __in LPVOID lpvReserved) {
	switch(fdwReason) {
		case DLL_PROCESS_ATTACH:
			hThread = CreateThread(NULL,	// lpThreadAttributes
					0,		// dwStackSize
					mainThread,	// lpStartAddress
					NULL,		// lpParameter
					0,		// dwCreationFlags (0==run right after creation)
					&threadId
					);
			break;
		case DLL_PROCESS_DETACH:
			//if (lpvReserved==NULL) {
			//	MessageBox(NULL, "Process DETACH due to FreeLibrary() call!", "durp", MB_OK);
			//} else {
			//	MessageBox(NULL, "Process DETACH due to process termination!", "durp", MB_OK);
			//}
			break;
		default:
			break;
	}
	
	return TRUE;
}
