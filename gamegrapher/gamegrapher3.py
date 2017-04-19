import matplotlib
matplotlib.use("TkAgg")
from ctypes import c_int, POINTER, windll, create_string_buffer, sizeof, byref
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from threading import Thread
from numpy import arange
import matplotlib.pyplot as plt
import matplotlib.animation, struct, time, sys
import tkinter as Tk
import numpy as np


class Gamegrapher:
    def __init__(self):
        self.version = "1.0"
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

    def appender(self):
        pid = int(input("Enter the pid: "))
        addr = int(input("Enter the address (not 0x..., but in hex): "),16)
        self.ly= []
        while True:
            time.sleep(1)
            self.y = Gamegrapher.get_value(self, pid, addr)
            self.ly.append(self.y)
            # There are alternatives here:
            # I was thinking of using arange, and continually expanding the range.
            # Alternatively, we can use the normal method of adding one to the list
            # As this will be threaded, there should be no problem. 
            
    def figure(self):
        Thread(target=Gamegrapher.appender(self), name = "Thread-2").start()
        self.f = Figure(figsize=(1,1), dpi=100) # Size of the figure presented; the nature of this is to be investigated
        self.a = f.add_subplot(111)
        self.k = len(self.ly)
        self.lx = arange(0,self.k,1)
        self.a.plot(self.lx,self.ly)
        self.canvas = FigureCanvasTkAgg(self.f, master=self.root)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        toolbar = NavigationToolbar2TkAgg(self.canvas, self.root)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

    def two(self):
        self.lx = arange(0,self.k,1)
        self.a.plot(self.lx,self.ly)        
        self.canvas.show()
        
    def grapher(self):
        self.root = Tk.Tk() # Creates the window, however still not shown
        self.root.wm_title("Statistical Analysis - Created by Ali Rassolie - %s" %self.version)
        Gamegrapher.figure(self)
        button = Tk.Button(master = root, text = "Update", command = lambda:Gamegrapher.two)
        button.pack(side = Tk.BOTTOM)
        Tk.mainloop
    
if __name__ == "__main__":
    x = Gamegrapher()
    Thread(target = x.grapher(), name = "Thread-1").start()    
    Thread(target = x.appender, name = "Thread-2").start()
