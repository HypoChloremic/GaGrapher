from threading import *
import threading

def hello():
    while True:
        print("Hello")
def world():
    while True:
        print("World")

Thread(group = None, target=hello, name = "Thread-1").start()
Thread(None, world, "Thread-2").start()
