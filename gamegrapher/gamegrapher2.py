import matplotlib
matplotlib.use("TkAgg")
from ctypes import c_int, POINTER, windll, create_string_buffer, sizeof, byref
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from threading import Thread
from numpy import arange
import matplotlib.pyplot as plt
import matplotlib.animation
import tkinter as Tk
import numpy as np
import struct
import time
import sys


version = "1.0"
lx, ly = [],[]
def get_value(pid, addr):
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

def appender():
    pid = int(input("Enter the pid: "))
    addr = int(input("Enter the address (not 0x..., but in hex): "),16)
    global ly
    ly, lx, x= [], [], 0
    while True:
        time.sleep(1)
        y = get_value(pid, addr)
        ly.append(y)
        # There are alternatives here:
        # I was thinking of using arange, and continually expanding the range.
        # Alternatively, we can use the normal method of adding one to the list
        # As this will be threaded, there should be no problem. 
        
def figure(root):
    #Thread(target=appender, name = "Thread-2").start()
    global ly, a2, canvas, k, a
    f = Figure(figsize=(1,1), dpi=100) # Size of the figure presented; the nature of this is to be investigated
    a = f.add_subplot(111)
    k = len(ly)
    lx = arange(0,k,1)
    a.plot(lx,ly)
    a2, = a.plot(lx,ly)
    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.show()
    canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
    toolbar = NavigationToolbar2TkAgg(canvas, root)
    toolbar.update()
    canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

def on_click_function():
    global ly, a2, canvas, k, a
    print("Button Pressed")
    k = float(len(ly))
    lx = arange(0,k,1)
    a.clear()
    a.plot(lx,ly)
    canvas.show()
    
    
def grapher():
    global version
    root = Tk.Tk() # Creates the window, however still not shown
    root.wm_title("Statistical Analysis - Created by Ali Rassolie - %s" %version)
    figure(root)
    button = Tk.Button(master = root, text="Update", command=lambda:on_click_function())
    button.pack(side=Tk.BOTTOM)
    Tk.mainloop
    
if __name__ == "__main__":
    Thread(target=appender, name = "Thread-2").start()
    time.sleep(5)
    Thread(target=grapher(), name = "Thread-1").start()    


