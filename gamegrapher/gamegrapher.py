from ctypes import c_int, POINTER, windll, create_string_buffer, sizeof, byref
import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np
import struct


w = 0
class Grapher:
    def get_value(self, pid, addr):
        #Store the size of an integer
        INT_SIZE = sizeof(c_int)

        #Open process with PROCESS_VM_OPERATION, PROCESS_VM_READ and PROCESS_VM_WRITE (the access required to read/write memory)
        k32 = windll.kernel32
        phnd = k32.OpenProcess(0x8|0x10|0x20, 0, pid) #(dwDesiredAccess, bInheritHandle, dwProcessId)

        #Create a buffer (which supposedly produces a mutable memory block) to receive the pointer value.
        int_buffer = create_string_buffer(INT_SIZE) 

        #Base address of the value

        #Deference pointer
        for i in range(4):
            k32.ReadProcessMemory(phnd, addr, byref(int_buffer), INT_SIZE, byref(c_int())) #(handle, baseaddr, buffer, buffer size, byte read)
            addr = struct.unpack("@i", int_buffer[::])[0]

        #Print the actual value
        k32.ReadProcessMemory(phnd, addr, byref(int_buffer), INT_SIZE, byref(c_int()))
        z = struct.unpack("@i", int_buffer[::])[0]
        #Pack data and write to memory
        #int_buffer = create_string_buffer(struct.pack("@i", 9999), INT_SIZE)
        #k32.WriteProcessMemory(phnd, addr, byref(int_buffer), INT_SIZE, byref(c_int())) #(handle, baseaddr, buffer, buffer size, byte read)

        #Close the handle and exit
        k32.CloseHandle(phnd)
        return float(z)

    def grapher(self):
        pid = int(input("Enter the pid: "))
        addr = int(input("Enter the address (not 0x..., but in hex): "),16)
        ly, lx= [], []
        
        fig = plt.figure()
        ax1 = fig.add_subplot(1,1,1)
        global w
        def g(self):
            global w
            k = Grapher.get_value(self, pid, addr)
            w += 1.0
            print(ly)
            print(lx)
            ly.append(k)
            lx.append(w)
            ax1.clear()
            ax1.plot(lx,ly)
        ani = matplotlib.animation.FuncAnimation(fig, g, interval = 30000)        
        plt.show()

if __name__ == "__main__":
    rm = Grapher()
    rm.grapher()
