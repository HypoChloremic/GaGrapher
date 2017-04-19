from ctypes import c_int, POINTER, windll, create_string_buffer, sizeof, byref
import struct




def get_value(pid, addr):
    #Store the size of an integer
    INT_SIZE = sizeof(c_int)

    #Open process with PROCESS_VM_OPERATION, PROCESS_VM_READ and PROCESS_VM_WRITE (the access required to read/write memory)
    k32 = windll.kernel32
    phnd = k32.OpenProcess(0x8|0x10|0x20, 0, pid) #(dwDesiredAccess, bInheritHandle, dwProcessId)

    #Create a buffer (which supposedly produces a mutable memory block) to receive the pointer value.
    int_buffer = create_string_buffer(INT_SIZE) 

    #Base address of the value
    #addr = 0x002CAB60

    #Deference pointer
    #for i in range(4):
        #k32.ReadProcessMemory(phnd, addr, byref(int_buffer), INT_SIZE, byref(c_int())) #(handle, baseaddr, buffer, buffer size, byte read)
        #addr = struct.unpack("@i", int_buffer[::])[0]
        #print(hex(addr), "points to...")

    #Print the actual value
    k32.ReadProcessMemory(phnd, addr, byref(int_buffer), INT_SIZE, byref(c_int()))
    print(struct.unpack("@i", int_buffer[::])[0])

    #Pack data and write to memory
    #int_buffer = create_string_buffer(struct.pack("@i", 9999), INT_SIZE)
    #k32.WriteProcessMemory(phnd, addr, byref(int_buffer), INT_SIZE, byref(c_int())) #(handle, baseaddr, buffer, buffer size, byte read)

    #Close the handle and exit
    k32.CloseHandle(phnd) 

get_value(2488, 0x002CAB60)
