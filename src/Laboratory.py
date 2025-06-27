import os
import ctypes
import sys
from Zone import *

class Laboratory():
    def __init__(self):
        usr32 = ctypes.windll.user32
        self.size1 = usr32.GetSystemMetrics(0)
        self.size2 = usr32.GetSystemMetrics(1)
        self.pax = self.size1/10
        self.pay = self.size2/10

    def getColorPanel():
        pass

if __name__ == "__main__":
    g = GraphicalInterpretor()
