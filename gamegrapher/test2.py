import ctypes, psutil, sys

kernel32 = ctypes.windll.kernel32

PROCESS_QUERY_INFORMATION = (0x0400)
PROCESS_VM_OPERATION = (0x0010)
PROCESS_VM_READ = (0x0008)
PROCESS_VM_WRITE = (0x0020)

OpenProcess = kernel32.OpenProcess
CloseHandle = kernel32.CloseHandle
GetLastError = kernel32.GetLastError
ReadProcessMemory = kernel32.ReadProcessMemory

class ReadWriteMemory:
    def OpenProcess(self, processName):
        dwDesiredAccess = PROCESS_QUERY_INFORMATION | PROCESS_VM_OPERATION | PROCESS_VM_READ | PROCESS_VM_WRITE 
        bInheritHandle = False
        hProcess = ctypes.windll.kernel32.OpenProcess(dwDesiredAccess, bInheritHandle, processName)
        if hProcess:
            return hProcess
        else:
            return None
                
    def CloseHandle(self, hProcess):
        CloseHandle(hObject)
        
    def GetLastError(self):
        GetLastError()
        return GetLastError()

    def ReadProcessMemory(self, hProcess, lpBaseAddress):
        try:
            lpBaseAddress = lpBaseAddress
            ReadBuffer = ctypes.c_uint()
            lpBuffer = ctypes.byref(ReadBuffer)
            nSize = ctyoes.sizeof(ReadBuffer)
            lpNumberOfBytesRead = ctypes.c_ulong(0) # Why 0?

            ReadProcessMemory(hProcess, lpBaseAddress, lpBuffer, nSize, lpNumberOfBytesRead)
            return ReadBuffer.value
        except (BufferError, ValueError, TypeError):
            CloseHandle(hProcess)
            e = "Handle Closed, Error ," + hprocess + GetLastError()
            return e


        
if __name__ == "__main__":
    rm = ReadWriteMemory()
    rm.OpenProcess("notepad.exe")
    
