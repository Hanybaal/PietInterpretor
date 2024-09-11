from pile import *
from output import *
from grille import *

class Programm():
    def __init__(self):
        self.grid = None
        self.stack = None
        self.output = None
        self.shareStack = False
        self.shareOutput = False
        self.fireStack = None
        self.fireOutput = None

    #Guetteurs
    def getStack(self):
        return self.stack

    def getOutput(self):
        return self.output

    def getGrid(self):
        return self.grid

    def sharingStack(self):
        return self.shareStack

    def sharingOutput(self):
        return self.shareOutput

    #Setteurs
    def setGrid(self, g = Grille(5, 5)):
        self.grid = g

    def setOutput(self, output):
        self.output = OutPut()
        self.output.output = output.output

    def setStack(self, stack):
        self.stack = Pile()
        self.stack.pile = list(stack.pile)
        self.stack.hauteur = stack.hauteur


    def blankInit(self):
        self.setGrid(Grille(5, 5))
        self.setOutput(OutPut())
        self.setStack(Pile())

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
