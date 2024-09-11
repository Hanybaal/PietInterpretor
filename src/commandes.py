

class Commandes():
    def __init__(self, dp, cc, output, stack):
        self.dp = dp
        self.cc = cc
        self.output = output
        self.stack = stack

    def inInt(self):
        self.stack.inInt()

    def inChar(self):
        self.stack.inChar()

    #Algos avec Output
    def outNum(self):
        v = self.stack.pop()
        self.output.outNum(v)

    def outChar(self):
        v = self.stack.pop()
        self.output.outChar(v)

    def switch(self, v):
        self.cc.switch(v)

    def pointer(self, v):
        self.dp.pointer(v)

    def empile(self, valeur):
        self.stack.empile(valeur)
        
    def push(self, block):
        self.stack.push(block)

    def pop(self):
        self.stack.pop()

    def add(self):
        self.stack.add()

    def substract(self):
        self.stack.substract()

    def multiply(self):
        self.stack.multiply()

    def divide(self):
        self.stack.divide()

    def mod(self):
        self.stack.mod()

    def nope(self):
        self.stack.nope()

    def greater(self):
        self.stack.greater()

    def duplicate(self):
        self.stack.duplicate()

    def roll(self):
        self.stack.roll()

    def inNum(self):
        self.stack.inInt()

    def inChar(self):
        self.stack.inChar()
