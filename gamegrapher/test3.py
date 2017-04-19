import ctypes, struct

def main():
    name = "MineSweeper.exe"

    pid = 456  # Minesweeper
    k = 0x8|0x10|0x20
    processHandle = ctypes.windll.kernel32.OpenProcess(k, False, pid)

    addr = 0x0E493BE8 # Minesweeper.exe module base address
    buffer = (ctypes.c_byte * 8)()
    bytesRead = ctypes.c_ulonglong()
    result = ctypes.windll.kernel32.ReadProcessMemory(processHandle, addr, buffer, len(buffer), ctypes.byref(bytesRead))
    e = ctypes.windll.kernel32.GetLastError()

    #print('result: ' + str(result) + ', err code: ' + str(e))
    #print('data: ' + str(struct.unpack('Q', buffer)[0]))

    ctypes.windll.kernel32.CloseHandle(processHandle)
    #return ("%s" %struct.unpack('Q', buffer)[0])
    a=1
    return a
    # Output:
main()
print(main())
