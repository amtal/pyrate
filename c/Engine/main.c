/* 
 *   When this implementation of d2py is injected into D2, it starts
 * a thread. The mainThread() function is the body of that thread. It should
 * initialize the Python interpreter and builtins, then start the 
 * actual bot by running the main Python script.
 */
#include <Python.h>
#include <windows.h>
#include <stdio.h>
#include "options.h"

#pragma comment(lib, "python26")

DWORD WINAPI mainThread(LPVOID lpArg)
{
	#ifdef MAKE_DEBUG_CONSOLE
	// Opens a console window for D2, which can be used to printf() data.
	// The Python interpreter has no access to this; which is fine, it will
	// use a Tk gui.
	FILE* stream;
	AllocConsole();	freopen_s(&stream, "conout$", "w", stdout);	
	#endif

	printf("Main d2py thread starting in process %d.\n", GetProcessId(GetCurrentProcess()));
	

	// Is this needed? Used to find the operating dir?
	//Py_SetProgramName("C:/Projects/2009 Summer/d2py/python/d2py.dll");
	
	Py_SetProgramName("d2py");
	Py_Initialize();
	PyEval_InitThreads(); // is it needed?
	printf("Python interpreter started!\n");

	// Dirty hack to initialize sys.argv[0], without which tkinter fails completely.
	// We currently rely on tkinter to serve as stdout.
	//
	// Hum, using the modified PyShell script solves that problem though. What was I doing wrong?
	//PyRun_SimpleString("import sys");
	//PyRun_SimpleString("sys.argv=['C:/Projects/2009 Summer/d2py/python/d2py.dll']");


	// Using PyRun_*File functions is a terrible idea due to FILE* structure being
	// compiler-dependant. The following method looks ugly, but seems to work.
	//
	// TODO: figure out how to set the directory this stuff runs in.
	//	 not a priority though, will fix that once the more interesting bits work!
	int ret = PyRun_SimpleString("exec(compile(open('D:/Projects/_2010 Spring/Pyrate/python/d2py.py').read(), 'd2py.py', 'exec'))"); // 80 chars 80 chars 80 chars
	
	//char* argv[3]={ "d2py.exe"
	//		, "\"D:/Projects/_2010 Spring/Pyrate/python/d2py.py\""
	//		, NULL;
	//		};
	//int ret = Py_Main(2, argv);

	// Looks like we ran out of things to do.
	printf("Main d2py thread finished (%d), cleaning and exiting.\n", ret);
	Py_Finalize();
	return 0;
}
