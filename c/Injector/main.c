/*
 *	Simple loader that injects a DLL with the same name (and directory) 
 * into the first instance of Game.exe that it finds.
 *	Rename the .exe file and .dll to something else to make it marginally
 * less trivial to detect.
 *
 * Credit: Darawk's tutorial, mostly.
 */
#include <windows.h>
#include <stdio.h>
#include <tlhelp32.h> 

#pragma comment(lib, "Advapi32")

// Pretty sure this is needed to mess with D2 process: if not, better safe than sorry.
int setDebugPrivilege() 
{
	HANDLE hToken;
	LUID seDebugNameValue;
	TOKEN_PRIVILEGES tp;

	if (!OpenProcessToken(GetCurrentProcess(),TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY, &hToken )) {
		printf("OpenProcessToken failed with error code %d.\n", GetLastError());
		return 1;
	}

	if (!LookupPrivilegeValue(NULL, SE_DEBUG_NAME, &seDebugNameValue )) {
		printf("LookupPrivilegeValue failed with error code %d.\n", GetLastError());
		CloseHandle(hToken); return 1;
	}

	tp.PrivilegeCount=1;
	tp.Privileges[0].Luid = seDebugNameValue;
	tp.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED;

	if (AdjustTokenPrivileges(hToken, FALSE, &tp, sizeof(tp), NULL, NULL )) {
		CloseHandle(hToken);
		return 0;
	} else {
		printf("AdjustTokenPrivileges failed with error code %d.\n", GetLastError());
		CloseHandle(hToken); return 1;
	}
} 

// Injects a DLL at path into the process with id pid.
//
// It kept failing in weird ways when I started the D2 process using CreateProcess so
// I just gave up and decided to start it from outside using a batch file or something.
int injectToPid(int pid, char* path) 
{
	HANDLE hProcess;
	PVOID mem;
	HANDLE hThread;
	HANDLE hLibrary;
	DWORD error;
	
	// Get a handle to the process we want to operate on.
	hProcess = OpenProcess(PROCESS_CREATE_THREAD | PROCESS_QUERY_INFORMATION | 
				PROCESS_VM_OPERATION | PROCESS_VM_WRITE | PROCESS_VM_READ, FALSE, pid);
	if (hProcess == INVALID_HANDLE_VALUE) {
		fprintf(stderr, "Cannot open pid: %d\n", pid);
		return 1;
	}
	
	// Allocate some memory inside that process.
	mem = VirtualAllocEx(hProcess, NULL, strlen(path) + 1, MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE);
	if (mem == NULL) {
		fprintf(stderr, "Can't allocate memory in process. %d\n", GetLastError());
		CloseHandle(hProcess);
		return 1;
	}
	
	// Write the path of the DLL we'll load to that memory. These two steps could be avoided
	// if we know a string address inside the target process. Then, a DLL can be loaded if it
	// has the same name as all or part of that string.
	if (WriteProcessMemory(hProcess, mem, (void*)path, strlen(path) + 1, NULL) == 0) {
		fprintf(stderr, "Can't write to memory in process.\n");
		VirtualFreeEx(hProcess, mem, strlen(path) + 1, MEM_RELEASE);
		CloseHandle(hProcess);
		return 1;
	}

	//  Create a thread inside the target process, and tell it to start executing in the 
	//LoadLibraryA function.
	//  We can pass one parameter to the thread, and luckily LL takes one parameter - the
	//path to the DLL.
	//  Might need to tweak this later: we need a way to pass the Python script path to the
	//DLL somehow...
	hThread = CreateRemoteThread(hProcess, NULL, 0, 
		(LPTHREAD_START_ROUTINE)GetProcAddress(GetModuleHandle("KERNEL32.DLL"),"LoadLibraryA"), mem, 0, NULL);
	if (hThread == INVALID_HANDLE_VALUE) {
		fprintf(stderr, "Can't create a thread in process.\n");
		VirtualFreeEx(hProcess, mem, strlen(path) + 1, MEM_RELEASE);
		CloseHandle(hProcess);
		return 1;
	}

	if (WaitForSingleObject(hThread, INFINITE)==WAIT_FAILED) {
		printf("WaitForSingleObject failed while waiting for RemoteThread to finish.\n");
		CloseHandle(hProcess);
		return 1;
	}

	//  Figure out what LoadLibrary returned by checking thread return value.
	hLibrary = NULL;
	if (!GetExitCodeThread(hThread, (LPDWORD)&hLibrary)) {
		printf("Can't get exit code for thread, GetLastError() = %i.\n", GetLastError());
		CloseHandle(hThread);
		VirtualFreeEx(hProcess, mem, strlen(path) + 1, MEM_RELEASE);
		CloseHandle(hProcess);
		return 1;
	}

	// Clean up.
	CloseHandle(hThread);
	VirtualFreeEx(hProcess, mem, strlen(path) + 1, MEM_RELEASE);

	// Check if we succeeded, find the error if not.
	if (hLibrary == NULL) {
		// All this for a GetLastError call...
		hThread = CreateRemoteThread(hProcess, NULL, 0, (LPTHREAD_START_ROUTINE) GetProcAddress(GetModuleHandle("KERNEL32.DLL"),"GetLastError"), 0, 0, NULL);
		if (hThread == INVALID_HANDLE_VALUE) {
			fprintf(stderr, "LoadLibraryA returned NULL and can't get last error.\n");
			CloseHandle(hProcess);
			return 1;
		}

		WaitForSingleObject(hThread, INFINITE);
		GetExitCodeThread(hThread, &error);

		CloseHandle(hThread);

		printf("LoadLibrary return NULL, GetLastError() is %i\n", error);
		CloseHandle(hProcess);
		return 1;
	}

	CloseHandle(hProcess);

	printf("Injected to %08x\n", (DWORD)hLibrary);
	
	return 0;
}

// Name is what shows up in Task Manager in the processes tab.
DWORD getIdFromName(char *procName)
{
   PROCESSENTRY32 pe;
   HANDLE thSnapshot;
   BOOL retval, ProcFound=FALSE;

   thSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);

   if(thSnapshot == INVALID_HANDLE_VALUE)  {
      printf("Error: unable to create toolhelp snapshot");
      exit(1);
   }

   pe.dwSize = sizeof(PROCESSENTRY32);

    retval = Process32First(thSnapshot, &pe);

   while(retval)   {
      if(strstr(pe.szExeFile, procName) )  {
         ProcFound = TRUE;
         break;
      }
      retval    = Process32Next(thSnapshot,&pe);
      pe.dwSize = sizeof(PROCESSENTRY32);
   }

   if (!ProcFound) {
	   printf("Process '%s' not found!\n", procName);
	   exit(1);
   }
   return pe.th32ProcessID;
} 

// CreateRemoteThread DLL injection is specific to Windows NT based OS.
int isWinNT() {return (GetVersion() < 0x80000000);}


int main(int argc, char* argv[])
{
	int pid,i; char path[MAX_PATH];

	// check OS compatibility
	if (!isWinNT()) {
		printf("Injector uses the CreateRemoteThread method, which \
			does not work outside Windows NT-based systems.");
		return 1;
	}

	// Full path name + extension of this program.
	if (!GetFullPathName(argv[0], MAX_PATH, path, NULL)) {
		printf("Couldn't get full path of executable. Error code %d.\n", GetLastError());
		return 1;
	}
	
	// DLL we inject will have the same name as the program. The name can then be modified
	// to remove one trivial way of detecting the bot.
	//
	// Might be a good idea to test that the user renames the thing in production versions...
	// But then again, natural selection has some merits.
	i = strlen(path);
	path[--i]='l'; path[--i]='l'; path[--i]='d';

	printf("Injecting: %s\n", path);

	setDebugPrivilege();
	pid = getIdFromName("Game.exe");
	injectToPid(pid, path);

	return 0;
}

