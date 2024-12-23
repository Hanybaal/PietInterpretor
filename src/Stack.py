from DirectionnalPointer import *

class Stack():
    def __init__(self):
        self.stack = []
        self.hauteur = 0

    def __repr__(self):
        return (str(self.stack))

    def afficher(self):
        print("--------------------")
        for p in self.stack:
            print(p)
            print("________")
        print("--------------------")

    def empty(self):
        return (self.stack == [])

    def reinit(self):
        self.stack = []
        self.hauteur = 0

    def empile(self, valeur):
        self.stack.append(valeur)
        self.hauteur += 1

    def push(self, block):
        self.empile(block.getValeur())

    def pop(self):
        if self.stack:
            v = self.stack[self.hauteur-1]
            self.stack.pop(self.hauteur-1)
            self.hauteur -= 1
            return v

        else:
            print("Pile vide!!")
            return 0

    def add(self):
        if (self.hauteur > 1):
            v1 = self.pop()
            v2 = self.pop()
            self.empile(int(v1) + int(v2))

        else:
            print("Addition impossible!!")

    def substract(self):
        if (self.hauteur > 1):
            v1 = self.pop()
            v2 = self.pop()
            self.empile(int(v1) - int(v2))

        else:
            print("Soustraction impossible!!")


    def multiply(self):
        if (self.hauteur > 1):
            v1 = self.pop()
            v2 = self.pop()
            self.empile(int(v1) * int(v2))

        else:
            print("Multiplication impossible!!")

    def divide(self):
        if (self.hauteur > 1):
            v1 = self.pop()
            v2 = self.pop()
            self.empile(int(v1)//int(v2))

        else:
            print("Soustraction impossible!!")

    def mod(self):
        if (self.hauteur > 1):
            v1 = self.pop()
            v2 = self.pop()
            self.empile(v1 % v2)

        else:
            print("Mod impossible!!")

    def nope(self):
        if self.stack:
            if self.top() == 0:
                self.replaceHeight(1)

            else:
                self.replaceHeight(0)
        else:
            print("Pile vide!!")

    def replaceHeight(self, valeur):
        if self.stack:
            self.stack[self.hauteur-1] = valeur


    def greater(self):
        if (self.hauteur > 1):
            v1 = self.pop()
            v2 = self.pop()
            if (int(v2) > int(v1)):
                self.empile(1)

            else:
                self.empile(0)

        else:
            print("Comparaison impossible!!")

    def duplicate(self):
        self.empile(self.top())

    def roll(self):
        v1 = self.pop()
        v2 = self.pop()
        self.empile(v1)
        self.empile(v2)

##Roll originel. Remplacé par un switch (caractère '/' en befunge)
##        v1 = self.pop()
##        v2 = self.pop()
##        p = self.stack[:v2]
##        for i in range(v1):
##            for j in range(len(p) - 1):
##                p[j], p[j + 1] = p[j + 1], p[j]
##
##        self.stack = p + self.stack[v2:]

    def inInt(self):
        v = int(input("Rentrez un nombre: "))
        self.inValid(v)

    def inValid(self, v):
        self.empile(v)

    def inChar(self):
        v = input("Rentrez un caractère: ")
        self.inValid(v)

    def top(self):
        return self.stack[self.hauteur-1]
