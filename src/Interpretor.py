from Stack import *
from Output import *
from Grid import *
from Color import *
from Controls import *
import time


class PietInterpretor():
    def __init__(self, grille, sets = None, stack = Stack(), output = Output()):
        self.allBlocks = []
        self.stack = stack
        self.grille = grille
        for line in self.grille.getGrid():
            for column in line:
                column.chercheVoisins(self.grille)
        self.output = output
        self.dp = DirectionnalPointer()
        self.cc = PointeurExtremite()
        self.cmd = Controls(self.dp, self.cc, self.output, self.stack)
        self.ordonnateur = Ordonnateur(self.cmd, sets)


    def lecture(self, grille, codel, nbEchecs = 0, speedyLector = False):
        couleur = codel.getColor()
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
            self.afficheStack()
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
            self.ordonnateur.change_cmd(newCell.getColor())

        else:
            self.ordonnateur.change_cmd(codel.getColor())

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

    def afficheStack(self):
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
    def __init__(self, cmd, sets = None):
        self.cmd = cmd
        if (sets is not None):
            self.colorTab = sets
        else:
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
                couls[-1].append(Color(couleur, luminosite))
        couls.append(Color(7, 0))
        couls.append(Color(8, 0))
        return couls

    def genere_tab_commandes(self, x, y):
        cmd = [[], [], [], [], [], []]
        #x2, y2 = c.x, c.y
        for i in range(6):
            for j in range(3):
                cmd[(i+y)%6].append(self.dico_cmd["c+" + str(i) + "+" + str((j-x)%3)])
        return cmd

    def change_cmd(self, newColor):
        if (Color.notAColor(newColor)):
            self.cmdTab = [[(None, "None") for i in range(3)] for j in range(6)]
            return

        x, y = self.getIndexColor(newColor)
        self.cmdTab = self.genere_tab_commandes(x, y)

    def getIndexColor(self, color):
        y = -1
        x = -1

        for line in self.colorTab[:-2]:
            y += 1
            x = -1
            for col in line:
                x += 1

                if (Color.sameColor(col, color)):
                    return (x, y)
              
        return (-1, -1)
        
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

        x, y = self.getIndexColor(couleur)

        return self.cmdTab[y][x][0]

    def actualCommandName(self, couleur):
        if (couleur.isWhite()):
            return "None"

        x, y = self.getIndexColor(couleur)
                
        return self.cmdTab[y][x][1]

    def printCmd(self):
        for cmd in self.cmdTab:
            t = ""
            for c in cmd:
                t += c[1] + " "*(12 - len(c[1]))

            print(t)

def _import(pgm):
    fichier = open(pgm, "r")
    
    # Lire les données du fichier sélectionné (ici un exemple de lecture)
    t = fichier.readlines()
    for c in range(len(t)):
        t[c] = t[c].replace('\n', '')

    ty = 0
    while (not ("EOP" in t[ty])):
        ty += 1

    tx = len(t[0].split(';'))
    grid = Grid(tx, ty)

    i, j = 0, -1
    line = t[0]
    while (not ("EOP" in t[i])):
        line = t[i]
        j = -1
        splitLine = line.split(';')
        for col in splitLine:
            j += 1
            color = col.split('/')
            grid.setCellule(i, j, Cellule(Color(int(color[0]), int(color[1])), j, i))

        i += 1


    #Recherche des voisins
    for ligne in range(len(grid.grille)):
        for colonne in range(len(grid.grille[ligne])):
            grid.grille[ligne][colonne].chercheVoisins(grid)

    fichier.close()
    
    return grid

g = _import("./../programmsBank/blank.txt")

if __name__ == "__main__":
    i = PietInterpretor(g)
    i.lecture(i.grille, i.grille.getGrid()[0][0])
