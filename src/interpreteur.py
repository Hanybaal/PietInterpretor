from pile import *
from output import *
from grille import *
from couleur import *
from commandes import *
import time


class InterpreteurPiet():
    def __init__(self, grille, stack = Pile(), output = OutPut()):
        self.allBlocks = []
        self.stack = stack
        self.grille = grille
        for line in self.grille.getGrille():
            for column in line:
                column.chercheVoisins(self.grille)
        self.output = output
        self.dp = PointeurDirectionnel()
        self.cc = PointeurExtremite()
        self.cmd = Commandes(self.dp, self.cc, self.output, self.stack)
        self.ordonnateur = Ordonnateur(self.cmd)


    def lecture(self, grille, codel, nbEchecs = 0, speedyLector = False):
        couleur = codel.getCouleur()
        commande = self.ordonnateur.actualCommand(couleur)
        nom = self.ordonnateur.actualCommandName(couleur)
        #On a une instruction à réaliser


        #On va construire le block lié à notre cellule et chercher la cellule de sortie
        blockActuel = Block()
        blockActuel.construit_block(codel)
        blockActuel.setValeur(len(blockActuel.block))
        self.allBlocks.append(blockActuel)
        dernierCodel = self.selectionne_codel(blockActuel)

        #Execution
        if (not speedyLector):
            print()
            print(nom)
            self.affichePile()
            self.afficheEtatDPCC()

        if commande != None and (nbEchecs == 0):
            if nom == "push":
                commande(self.allBlocks[-2])

            elif nom == "pointer" or nom == "switch":
                commande(self.stack.pop())

            else:
                commande()


        newCell = dernierCodel

        x, y = dernierCodel.getX(), dernierCodel.getY()
        dx, dy = self.dp.direction_actuelle()[0], self.dp.direction_actuelle()[1]
        if self.grille.sortie(x + dx, y + dy):
            nbEchecs = self.rouleNbEchecs(nbEchecs)

        else:
            newCell = grille.getCellule(y + dy, x + dx)
            if newCell.isBlack():
                newCell = dernierCodel
                nbEchecs = self.rouleNbEchecs(nbEchecs)

            else:
                nbEchecs = 0

        if self.maxEchecs(nbEchecs):
            return

        #On modifie le tableau pour pouvoir interpréter la prochaine couleur
        if (self.allBlocks[-1].isWhite()):
            self.ordonnateur.change_cmd(newCell.getCouleur())

        else:
            self.ordonnateur.change_cmd(codel.getCouleur())

        if (not speedyLector):
            time.sleep(1)

        self.lecture(grille, newCell, nbEchecs, speedyLector)

    def lancerCommande(commande, blockActuel):
        if nom == "push":
            commande(blockActuel)

        elif nom == "pointer" or nom == "switch":
            commande(blockActuel.getValeur())

        else:
            commande()

    def afficheEtatDPCC(self):
        self.dp.afficheEtat()
        self.cc.afficheEtat()

    def affichePile(self):
        self.stack.afficher()

    def maxEchecs(self, n):
        return (n > 8)

    def rouleNbEchecs(self, nbEchecs):
        if (nbEchecs == 3 or nbEchecs == 7):
            self.cc.roule()
            self.dp.roule()

        else:
            self.dp.roule()

        return (nbEchecs + 1)

    #En Piet, le codel d'un block est choisi de la manière suivante:
    #- On regarde le codel à l'extrême dans le sens du DP
    #- On regarde le codel le plus extrême dans le sens du CC
    #(voire tableau récapitulatif):
    def selectionne_codel(self, block):
        direcAct = self.dp.direction_actuelle()
        extrChois = self.cc.extremite_choisie(self.dp)
        cell = None

        if direcAct[0] == 1:
            cellMaxX = block.maxix()
            if extrChois == 1:
                cell = block.plus_bas(cellMaxX)

            else:
                cell = block.plus_haut(cellMaxX)

        elif direcAct[0] == -1:
            cellMinX = block.minx()
            if extrChois == 1:
                cell = block.plus_haut(cellMinX)

            else:
                cell = block.plus_bas(cellMinX)


        if direcAct[1] == 1:
            cellMaxY = block.maxiy()
            if extrChois == 1:
                cell = block.plus_gauche(cellMaxY)

            else:
                cell = block.plus_droite(cellMaxY)

        elif direcAct[1] == -1:
            cellMinY = block.miny()
            if extrChois == 1:
                cell = block.plus_droite(cellMinY)

            else:
                cell = block.plus_gauche(cellMinY)

        return cell



class Ordonnateur():
    def __init__(self, cmd):
        self.cmd = cmd
        self.colorTab = self.creaColorTab()
        self.cmdTab = [[(None, "None") for i in range(3)] for j in range(6)]
        self.pointeurx = None
        self.pointeury = None
        self.dico_cmd = {"c+0+0" : (None, "None"),
                         "c+1+0" : (lambda : self.cmd.add(), "add"),
                         "c+2+0" : (lambda : self.cmd.divide(), "div"),
                         "c+3+0" : (lambda : self.cmd.greater(), " > "),
                         "c+4+0" : (lambda : self.cmd.duplicate(), "dup"),
                         "c+5+0" : (lambda : self.cmd.inChar(), "in(char)"),
                         "c+0+1" : (lambda block : self.cmd.push(block), "push"),
                         "c+1+1" : (lambda : self.cmd.substract(), "sub"),
                         "c+2+1" : (lambda : self.cmd.mod(), "mod"),
                         "c+3+1" : (lambda v : self.cmd.pointer(v), "pointer"),
                         "c+4+1" : (lambda : self.cmd.roll(), "roll"),
                         "c+5+1" : (lambda : self.cmd.outChar(), "out(char)"),
                         "c+0+2" : (lambda : self.cmd.pop(), "pop"),
                         "c+1+2" : (lambda : self.cmd.multiply(), "mul"),
                         "c+2+2" : (lambda : self.cmd.nope(), "not"),
                         "c+3+2" : (lambda v : self.cmd.switch(v), "switch"),
                         "c+4+2" : (lambda : self.cmd.inNum(), "in(num)"),
                         "c+5+2" : (lambda : self.cmd.outNum(), "out(num)")}

    def creaColorTab(self):
        couls = []
        for couleur in range(1, 7):
            couls.append([])
            for luminosite in range(1, 4):
                couls[-1].append(Couleur(couleur, luminosite))
        couls.append(Couleur(7, 0))
        couls.append(Couleur(8, 0))
        return couls

    def genere_tab_commandes(self, couleur):
        cmd = [[], [], [], [], [], []]
        y, x = couleur.getCouleur() - 1, couleur.getLuminosite() - 1
        #x2, y2 = c.x, c.y
        for i in range(6):
            for j in range(3):
                cmd[(i+y)%6].append(self.dico_cmd["c+" + str(i) + "+" + str((j-x)%3)])
        return cmd

    def change_cmd(self, newColor):
        if (Couleur.notACouleur(newColor)):
            self.cmdTab = [[(None, "None") for i in range(3)] for j in range(6)]
            return
        self.cmdTab = self.genere_tab_commandes(newColor)

    def rotationLuminosite(self):
        for colonne in range(6):
            for ligne in range(2):
                self.swap(ligne, colonne, -1, colonne)

    def rotationColor(self):
        for ligne in range(3):
            for colonne in range(5):
                self.swap(ligne, colonne, ligne, -1)


    def swap(self, i1, j1, i2, j2):
        t = self.cmdTab
        t[i1][j1], t[i2][j2] = t[i2][j2], t[i1][j1]

    def actualCommand(self, couleur):
        if (couleur.isWhite()):
            return None

        x = couleur.getLuminosite() - 1
        y = couleur.getCouleur() - 1
        return self.cmdTab[y][x][0]

    def actualCommandName(self, couleur):
        if (couleur.isWhite()):
            return "None"
        x = couleur.getLuminosite() - 1
        y = couleur.getCouleur() - 1
        return self.cmdTab[y][x][1]

    def printCmd(self):
        for cmd in self.cmdTab:
            t = ""
            for c in cmd:
                t += c[1] + " "*(12 - len(c[1]))

            print(t)

fichier = open("./../programmsBank/blank.txt", "r")

t = fichier.readlines()
x = len(t[-1])//2
y = len(t)
g = Grille(x, y)
for ligne in range(len(g.grille)):
    for colonne in range(len(g.grille[ligne])):
        g.grille[ligne][colonne] = Cellule(
            Couleur(int(t[ligne][colonne*2]), int(t[ligne][colonne*2+1])), colonne, ligne)

for ligne in range(len(g.grille)):
    for colonne in range(len(g.grille[ligne])):
        g.grille[ligne][colonne].chercheVoisins(g)

fichier.close()

if __name__ == "__main__":
    i = InterpreteurPiet(g)
    i.lecture(i.grille, i.grille.getGrille()[0][0])
