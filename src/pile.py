from PointeurDirectionel import *

class Pile():
    def __init__(self):
        self.pile = []
        self.hauteur = 0


    def __repr__(self):
        return (str(self.pile))

    def afficher(self):
        print("--------------------")
        for p in self.pile:
            print(p)
            print("________")
        print("--------------------")

    def empty(self):
        return (self.pile == [])

    def reinit(self):
        self.pile = []
        self.hauteur = 0

    def empile(self, valeur):
        self.pile.append(valeur)
        self.hauteur += 1

    def push(self, block):
        self.empile(block.getValeur())

    def pop(self):
        if self.pile:
            v = self.pile[self.hauteur-1]
            self.pile.pop(self.hauteur-1)
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
        if self.pile:
            if self.sommet() == 0:
                self.replace_hauteur(1)

            else:
                self.replace_hauteur(0)
        else:
            print("Pile vide!!")

    def replace_hauteur(self, valeur):
        if self.pile:
            self.pile[self.hauteur-1] = valeur


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
        self.empile(self.sommet())

    def roll(self):
        v1 = self.pop()
        v2 = self.pop()
        self.empile(v1)
        self.empile(v2)

##Roll originel. Remplacé par un switch (caractère '/' en befunge)
##        v1 = self.pop()
##        v2 = self.pop()
##        p = self.pile[:v2]
##        for i in range(v1):
##            for j in range(len(p) - 1):
##                p[j], p[j + 1] = p[j + 1], p[j]
##
##        self.pile = p + self.pile[v2:]

    def inInt(self):
        v = int(input("Rentrez un nombre: "))
        self.inValid(v)

    def inValid(self, v):
        self.empile(v)

    def inChar(self):
        v = input("Rentrez un caractère: ")
        self.inValid(v)

    def sommet(self):
        return self.pile[self.hauteur-1]
