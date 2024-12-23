from Color import *

class Grid():
    def __init__(self, taillex, tailley):
        self.taillex = taillex
        self.tailley = tailley
        self.grille = [[Cellule(Color(7, 0), x, y) for x in range(taillex)] for y in range(tailley)]

    def __repr__(self):
        txt = ""
        nbespaces = 0
        for y in range(self.tailley):
            for x in range(self.taillex):
                txt += str(self.getGrid()[y][x])
                nbespaces = 3 - len(str(self.getGrid()[y][x]))
                txt += " "*nbespaces
                txt += "    "
            txt += '\n'
        return txt

    def sortie(self, x, y):
        return (x < 0 or y < 0 or x > self.maxX() or y > self.maxY() or self.getCellule(y, x).isBlack())

    def getGrid(self):
        return self.grille

    def getRow(self, y):
        return self.grille[y]

    def getCellule(self, y, x):
        return self.grille[y][x]

    def maxX(self):
        return (len(self.getGrid()[0]) - 1)

    def maxY(self):
        return (len(self.getGrid()) - 1)


class Cellule():
    def __init__(self, couleur, x, y):
        self.color = couleur
        self.x, self.y = x, y
        self.voisins = []
        self.commande = None

    def __repr__(self):
        return (self.color.hexa)
        #str(self.y) + str(self.x) + ": " +

    def change_couleur(self, couleur):
        self.color = couleur

    def chercheVoisins(self, grid):
        grille = grid.getGrid()
        if self.getX() > 0:
            self.voisins.append(grille[self.y][self.x - 1])

        if self.getX() < grid.maxX():
            self.voisins.append(grille[self.y][self.x + 1])

        if self.getY() > 0:
            self.voisins.append(grille[self.y - 1][self.x])

        if self.getY() < grid.maxY():
            self.voisins.append(grille[self.y + 1][self.x])


    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getColor(self):
        return self.color

    def isBlack(self):
        return (self.getColor().getColor() == 8)

    def isWhite(self):
        return (self.getColor().getColor() == 7)


class Block():
    def __init__(self):
        self.block = []
        self.valeur = 0

    def construit_block(self, celluleActuelle):
        self.block.append(celluleActuelle)
        for v in celluleActuelle.voisins:
            if self.identiqueColor(v, celluleActuelle) and not(v in self.block):
                self.construit_block(v)


    def identiqueColor(self, v, celluleActuelle):
        b1 = (v.color.getColor() == celluleActuelle.color.getColor())
        b2 = (v.color.getLuminosity() == celluleActuelle.color.getLuminosity())
        return (b1 and b2)

    def getColor(self):
        return self.block[0].getColor().getColor()

    def isWhite(self):
        return (self.getColor() == 7)

    def setValeur(self, v):
        self.valeur = v

    def getValeur(self):
        return self.valeur

    def liste_des_x(self):
        return [cel.getX() for cel in self.block]

    def liste_des_y(self):
        return [cel.getY() for cel in self.block]


    def maxix(self):
        maxi = self.block[0]
        for m in self.block:
            if m.getX() > maxi.getX():
                maxi = m

        return maxi


    #Appel du DP
    def minx(self):
        mini = self.block[0]
        for m in self.block:
            if m.getX() < mini.getX():
                mini = m

        return mini

    def maxiy(self):
        maxi = self.block[0]
        for m in self.block:
            if m.getY() > maxi.getY():
                maxi = m

        return maxi

    def miny(self):
        mini = self.block[0]
        for m in self.block:
            if m.getY() < mini.getY():
                mini = m

        return mini


    #Appel du CC
    def plus_droite(self, cel):
        droite = cel
        for c in self.block:
            if c.getY() == droite.getY() and c.getX() > droite.getX():
                droite = c

        return droite

    def plus_gauche(self, cel):
        gauche = cel
        for c in self.block:
            if c.y == gauche.y and c.getX() < gauche.getX():
                droite = c

        return gauche

    def plus_bas(self, cel):
        bas = cel
        for c in self.block:
            if c.getX() == bas.getX() and c.getY() > bas.getY():
                bas = c

        return bas

    def plus_haut(self, cel):
        haut = cel
        for c in self.block:
            if c.getX() == haut.getX() and c.getY() < haut.getY():
                haut = c

        return haut
