from threading import Thread

#lx = 0
def function():
    lx = 0
    while True:
        global lx # We are referring to the globally assigned variable.
        lx+=1
        #return lx
        
def function1():
    while True:
        global lx # We are referring to the globally assigned variable.
        print(lx)

#Thread(target=function).start()
#Thread(target=function1).start()


def a():
    lx=1
    global lx
    print(lx)
def a2():
    global lx
    print(lx)
a()
a2()
