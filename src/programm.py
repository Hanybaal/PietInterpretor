from Stack import *
from Output import *
from Grid import *

class Programm():
    def __init__(self):
        self.grid = None
        self.sets = None
        self.stack = None
        self.output = None
        self.shareStack = False
        self.shareOutput = False
        self.fireStack = None
        self.fireOutput = None
        self.name = "Unamed"

    #Guetteurs
    def getStack(self):
        return self.stack

    def getOutput(self):
        return self.output

    def getGrid(self):
        return self.grid

    def getSets(self):
        return self.sets

    def sharingStack(self):
        return self.shareStack

    def sharingOutput(self):
        return self.shareOutput

    #Setteurs
    def setGrid(self, g = Grid(5, 5)):
        self.grid = g

    def setSets(self, sets = None):
        self.sets = sets

    def setOutput(self, output):
        self.output = Output()
        self.output.output = output.output
        self.output.lines = list(output.lines)
        self.output.cursor = output.cursor

    def setStack(self, stack):
        self.stack = Stack()
        self.stack.stack = list(stack.stack)
        self.stack.hauteur = stack.hauteur

    def blankInit(self):
        self.setGrid(Grid(5, 5))
        self.setOutput(Output())
        self.setStack(Stack())
        self.setSets(None)

    def setFires(self, f1, f2):
        self.fireStack = f1
        self.fireOutput = f2

    def changeStackState(self, can):
        self.shareStack = not self.shareStack
        if (self.fireStack is not None):
            can.itemconfigure(self.fireStack,
                              fill = ("green" if self.sharingStack() else "red"))

    def changeOutputState(self, can):
        self.shareOutput = not self.shareOutput
        if (self.fireOutput is not None):
            can.itemconfigure(self.fireOutput,
                              fill = ("green" if self.sharingOutput() else "red"))

    def partialReset(self):
        self.stack = Stack()
        self.output = Output()
