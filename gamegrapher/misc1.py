from threading import Thread

lx = 0
def function():
    while True:
        global lx # We are referring to the globally assigned variable.
        lx+=1
        #return lx
        
def function1():
    
    while True:
        global lx # We are referring to the globally assigned variable.
        print(lx)

Thread(target=function).start()
Thread(target=function1).start()
