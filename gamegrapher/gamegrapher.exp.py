import matplotlib
matplotlib.use('TkAgg')

from numpy import arange, sin, pi # Here is arange
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import sys
import tkinter as Tk

root = Tk.Tk() # This creates a window
root.wm_title("Grapher") # This creates the title


f = Figure(figsize=(5, 4), dpi=100) # The size of the Figure; the nature of this class is unknown as of yet.
a = f.add_subplot(111)              # The standard stuff
t = arange(0.0, 3.0, 0.01)          # Is inherent to numpy; arange(start, stop, step, dtype=None)
s = sin(2*pi*t)                     # This was imported earlier

a.plot(t, s)


# a tk.DrawingArea
canvas = FigureCanvasTkAgg(f, master=root)
canvas.show()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

toolbar = NavigationToolbar2TkAgg(canvas, root)
toolbar.update()
canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)


def on_key_event(event):
    print('you pressed %s' % event.key)
    key_press_handler(event, canvas, toolbar)

canvas.mpl_connect('key_press_event', on_key_event)


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

button = Tk.Button(master=root, text='Quit', command=_quit)
button.pack(side=Tk.BOTTOM)

Tk.mainloop()
# If you put root.destroy() here, it will cause an error if
# the window is closed with the window manager.
