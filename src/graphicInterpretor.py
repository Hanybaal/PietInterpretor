from Theme import *
from Interpretor import *
from Zone import *
from GraphicZone import *
import tkinter as tk
from math import *
from random import randint
import os
import ctypes
import sys
from tkinter import filedialog


class GraphicalInterpretor(PietInterpretor):
    def __init__(self, fen = None, main = None, grille = Grid(5, 5), ptc = 0,
                 launched = False, isLast = False, stack = Stack(), output = Output()):
        super().__init__(grille, stack, output)

        self.main = main
        self.programmName = "Unamed"
        self.programmToChange = ptc

        usr32 = ctypes.windll.user32
        self.size1 = usr32.GetSystemMetrics(0)
        self.size2 = usr32.GetSystemMetrics(1)
        self.pax = self.size1/10
        self.pay = self.size2/10

        self.fen = fen
        if (self.fen == None):
            self.fen = tk.Tk()

        self.fen.attributes('-fullscreen', True)
        self.fen.maxsize(self.size1, self.size2)
        self.fen.minsize(self.size1, self.size2)
        self.fen.bind('<Key>', self.keyboardEvents)

        self.codeZone = None
        self.nbDrawingWidgets = 8
        self.nbElementsInStack = 10
        self.actualColor = Color(7, 0)
        self.mode = "single"
        self.inp = None
        self.goodInput = tk.BooleanVar()
        self.goodInput.set(False)
        self.pause = tk.IntVar()
        self.pause.set(0)
        self.speed = 1000
        self.respeed = None
        self.firstLine = 0
        self.widgets()
        self.majOutput()

        self.launched = launched
        self.isLast = isLast
        if (launched):
            self.speed = 1
            self.lecture(self.grille, self.grille.getCellule(0, 0))

        self.fen.mainloop()

    def lecture(self, grille, codel, nbEchecs = 0):
        if ((self.mode == "reset") or (self.mode == "stop")):
            self.output.reinit()
            self.majOutput()
            self.mode = "normal"
            return

        if (self.mode == "pause"):
            self.mode = "pause"

            if (self.main is not None):
                self.main.fen.wait_variable(self.pause)
            else:
                self.fen.wait_variable(self.pause)

            self.mode = "normal"

        self.cleanGrid()

        if (codel.isBlack()):
            return

        self.majCodelLector(codel)
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
        self.majStack()

        if commande != None and (nbEchecs == 0):
            if nom == "push":
                commande(self.allBlocks[-2])

            elif nom == "pointer" or nom == "switch":
                #commande(blockActuel.getValeur())
                commande(self.stack.pop())

            elif nom == "in(char)" or nom == "in(num)":
                self.mode = nom

                if (self.main is not None):
                    self.main.fen.wait_variable(self.goodInput)

                else:
                    self.fen.wait_variable(self.goodInput)

                self.mode = "normal"
                self.goodInput.set(False)

            else:
                commande()

        if ("out" in nom):
            self.majOutput()

        newCell = dernierCodel
        x, y = dernierCodel.getX(), dernierCodel.getY()
        dx, dy = self.dp.direction_actuelle()[0], self.dp.direction_actuelle()[1]
        if self.grille.sortie(x + dx, y + dy):
            nbEchecs = self.rouleNbEchecs(nbEchecs)

        else:
            newCell = grille.getCellule(y + dy, x + dx)
            nbEchecs = 0

        if self.maxEchecs(nbEchecs):
            if (self.launched and (not self.isLast)):
                self.quit()
            return

        #On modifie le tableau pour pouvoir interpréter la prochaine couleur
        if (self.allBlocks[-1].isWhite()):
            self.ordonnateur.change_cmd(newCell.getColor())

        else:
            self.ordonnateur.change_cmd(codel.getColor())

        self.can.update()
        self.fen.after(self.speed, lambda : self.lecture(grille, newCell, nbEchecs))
        #self.lecture(grille, newCell, nbEchecs)


########################################################################################
##### Fonctions D'Etat #################################################################
########################################################################################
    def _export(self):
        # Demander à l'utilisateur de choisir un emplacement pour enregistrer le fichier
        fichier_destination = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Fichiers texte", "*.txt"),
                                                ("Tous les fichiers", "*.*")])

        # Écrire des données dans le fichier (ici un exemple avec une chaîne de texte)
        if fichier_destination:
            with open(fichier_destination, "w") as fichier:
                for line in self.grille.getGrid():
                    for cellule in line:
                        couleur = cellule.getColor()
                        fichier.write(str(couleur.getColor()))
                        fichier.write(str(couleur.getLuminosity()))

                    fichier.write(chr(10))

        self.programmName = os.path.basename(fichier_destination)[:-4] #txt en moins

        if (self.main != None):
            self.main.rename(self.programmName)

    def countMinus(self, txt):
        s = 0
        for i in range(len(txt)):
            if (txt[i] == '-'):
                s += 1
        return s

    def _import(self):
        # Demander à l'utilisateur de choisir un fichier à importer
        fichier_source = filedialog.askopenfilename(filetypes=[("Fichiers texte", "*.txt"),
                                                   ("Tous les fichiers", "*.*")])

        # Lire les données du fichier sélectionné (ici un exemple de lecture)
        if fichier_source:
            self.programmName = os.path.basename(fichier_source)[:-4] #txt en moins

            if (self.main != None):
                self.main.rename(self.programmName)

            fichier = open(fichier_source, "r")
            t = fichier.readlines()
            for c in range(len(t)):
                t[c] = t[c][:-1]

            x = len(t[-1])//2
            if ('-' in t[-1]):
                s = self.countMinus(t[-1])
                x = (len(t[-1]) - s)//2

            y = len(t)
            g = Grid(x, y)
            nbMoins = 0
            for ligne in range(len(g.grille)):
                nbMoins = 0
                for colonne in range(len(g.grille[ligne])):
                    w1 = t[ligne][colonne*2 + nbMoins]
                    if (w1 == '-'):
                        w1 = t[ligne][colonne*2 + nbMoins] + t[ligne][colonne*2 + nbMoins + 1]
                        nbMoins += 1

                    w2 = t[ligne][colonne*2 + nbMoins + 1]
                    if (w2 == '-'):
                        w2 = t[ligne][colonne*2 + nbMoins + 1] + t[ligne][colonne*2 + nbMoins + 2]
                        nbMoins += 1

                    g.grille[ligne][colonne] = Cellule(Color(int(w1), int(w2)),
                                                               colonne, ligne)


            for ligne in range(len(g.grille)):
                for colonne in range(len(g.grille[ligne])):
                    g.grille[ligne][colonne].chercheVoisins(g)

            fichier.close()

            self.grille = g

            self.reinit()
            self.can.delete("codeZone")
            self.grille = g

            self.codeZone.underZones = []
            self.makeCodeZone(self.codeZone)
            self.colorZone(self.zone2)

            codeZone = self.codeZone

            ########## décorations ##########
            codeZoneExtr = [(codeZone.getX(), codeZone.getY()),
                            (codeZone.getEndX(), codeZone.getY()),
                            (codeZone.getEndX(), codeZone.getEndY()),
                            (codeZone.getX(), codeZone.getEndY())]

            zone2Extr = [(self.zone2.getX(), self.zone2.getY()),
                         (self.zone2.getEndX(), self.zone2.getY()),
                         (self.zone2.getEndX(), self.zone2.getEndY()),
                         (self.zone2.getX(), self.zone2.getEndY())]

            scze = len(codeZoneExtr)
            w = 2
            c = "black"
            for i in range(len(codeZoneExtr)):
                self.can.create_line(codeZoneExtr[i][0], codeZoneExtr[i][1],
                                     zone2Extr[i][0], zone2Extr[i][1],
                                     fill = c, width = w,
                                     tags = "codeZone")

                self.can.create_line(codeZoneExtr[(i+1)%scze][0], codeZoneExtr[(i+1)%scze][1],
                                     zone2Extr[i][0], zone2Extr[i][1],
                                     fill = c, width = w,
                                     tags = "codeZone")

                self.can.create_line(codeZoneExtr[(i-1)%scze][0], codeZoneExtr[(i-1)%scze][1],
                                     zone2Extr[i][0], zone2Extr[i][1],
                                     fill = c, width = w,
                                     tags = "codeZone")

    def reinit(self):
        self.programmName = "Unamed"
        self.allBlocks = []
        self.mode = "single"
        self.actualColor = Color(7, 0)
        self.dp.reinit()
        self.cc.reinit()
        self.ordonnateur = Ordonnateur(self.cmd)
        #self.ordonnateur.change_cmd(Color(-1, -1))
        self.firstLine = 0
        self.stack.reinit()
        self.output.reinit()
        self.majOutput()
        self.majStack()

    def reset(self, x = 5, y = 5):
        gx, gy = self.sizeCodeX.get(), self.sizeCodeY.get()
        x = int(gx) if gx.isnumeric() else x
        y = int(gy) if gy.isnumeric() else y

        self.reinit()
        self.can.delete("codeZone")
        self.grille = Grid(x, y)
        for line in self.grille.getGrid():
            for column in line:
                column.chercheVoisins(self.grille)

        self.codeZone.underZones = []
        self.makeCodeZone(self.codeZone)
        self.colorZone(self.zone2)

        codeZone = self.codeZone

        ########## décorations ##########
        codeZoneExtr = [(codeZone.getX(), codeZone.getY()),
                        (codeZone.getEndX(), codeZone.getY()),
                        (codeZone.getEndX(), codeZone.getEndY()),
                        (codeZone.getX(), codeZone.getEndY())]

        zone2Extr = [(self.zone2.getX(), self.zone2.getY()),
                     (self.zone2.getEndX(), self.zone2.getY()),
                     (self.zone2.getEndX(), self.zone2.getEndY()),
                     (self.zone2.getX(), self.zone2.getEndY())]

        scze = len(codeZoneExtr)
        w = 2
        c = "black"
        for i in range(len(codeZoneExtr)):
            self.can.create_line(codeZoneExtr[i][0], codeZoneExtr[i][1],
                                 zone2Extr[i][0], zone2Extr[i][1],
                                 fill = c, width = w,
                                 tags = "codeZone")

            self.can.create_line(codeZoneExtr[(i+1)%scze][0], codeZoneExtr[(i+1)%scze][1],
                                 zone2Extr[i][0], zone2Extr[i][1],
                                 fill = c, width = w,
                                 tags = "codeZone")

            self.can.create_line(codeZoneExtr[(i-1)%scze][0], codeZoneExtr[(i-1)%scze][1],
                                 zone2Extr[i][0], zone2Extr[i][1],
                                 fill = c, width = w,
                                 tags = "codeZone")
        ################################################################################

        if (self.main != None):
            lc = self.main.lastCode
            self.main.programms[lc].grid = self.grille
            self.main.programms[lc].stack = self.stack
            self.main.programms[lc].output = self.output



    def convertIntoMode(self, x):
        if (x == 0):
            return "single"

        if (x == 1):
            return "recursive"

        if (x == 3):
            return "reset"

        if (x == 4):
            return "stop"

        if (x == 5):
            return "pause"

        if (x == 6):
            return "import"

        if (x == 7):
            return "export"

        return "start"

    def pauseMode(self):
        if (self.pause.get() == 0):
            self.pause.set(1)
            self.mode = "pause"

        else:
            self.pause.set(0)
            self.mode = "normal"

    def newSpeed(self, event):
        self.speed = self.respeed.get()

    def waitReturn(self, v):
        if (self.main is not None):
            self.main.fen.wait_variable(v)
        else:
            self.fen.wait_variable(v)

    def validInput(self, event = None):
        value = self.inp.get()

        if ((value != "") and ((self.mode == "in(num)") or (self. mode == "in(char)"))):
            if (self.mode == "in(num)"):
                if not (value.isnumeric()):
                    return

            elif (self.mode == "in(char)"):
                if (value.isnumeric() or (len(value) > 1)):
                    return

            self.goodInput.set(True)
            self.stack.inValid(value)
            return
        return

    def whatCodeZoneIsChoosed(self, x, y):
        codeTable = self.zone2.underZones[0]
        sx = len(self.grille.grille[0])
        sy = len(self.grille.grille)
        z = int((x - codeTable.getX())*sx/(codeTable.getSizeX()))
        z += int((y - codeTable.getY())*sy/(codeTable.getSizeY()))*sx
        z = int(z)
        return (codeTable.underZones[z], z)


    def whatZoneIsChoosed(self, x, y):
        zone = None
        colorTab = self.zone1.underZones[-1]
        size = len(colorTab.underZones)
        for z in range(size):
            self.can.itemconfigure(colorTab.underZones[z].graphicZone,
                                   fill = colorTab.underZones[z].getColor())
            if Zone.inZone(colorTab.underZones[z], x, y):
                zone = z

        if (zone is None):
            return None

        self.can.itemconfigure(colorTab.underZones[zone].graphicZone, fill = "gray73")

        return (zone if (zone < (size - 2)) else (zone - size))

    def whatSetZoneIsChoosed(self, x, y):
        zone = None
        setsTab = self.zone1.underZones[-2]
        size = len(setsTab.underZones)
        for z in range(size):
            self.can.itemconfigure(setsTab.underZones[z].graphicZone,
                                   fill = setsTab.underZones[z].getColor())
            if Zone.inZone(setsTab.underZones[z], x, y):
                zone = z

        if (zone is None):
            return None

        return setsTab.underZones[zone]

########################################################################################
##### Fonctions évènementielles ########################################################
########################################################################################
    def changeSetColor(self, event):
        selectedSet = self.whatSetZoneIsChoosed(event.x, event.y)
        if (selectedSet is None):
            return

        #On a sélectionné le menu déroulant d'une des couleurs        
        print(selectedSet.getColor())

    def scroll(self, direction):
        #Si un des deux boutons de la scrollBar est pressé:
        #*** Saute une ligne ou la remet dans l'output
        self.firstLine += direction
        if (self.firstLine < 0):
            self.firstLine = 0
            return
        self.majOutput()

    def chosenWidget(self, event):
        widgetZone = self.zone1.underZones[1]

        for i in range(len(widgetZone.underZones)):
            self.can.itemconfigure(widgetZone.underZones[i].graphicZone, fill = "plum3")

        x = int((event.x - widgetZone.getX())*self.nbDrawingWidgets/widgetZone.getSizeX())
        self.can.itemconfigure(widgetZone.underZones[x].graphicZone,
                               fill = "white smoke")

        self.mode = self.convertIntoMode(x)
        if (self.mode == "start"):
            self.reinit()
            self.lecture(self.grille, self.grille.getCellule(0, 0))

        if (self.mode == "reset"):
            self.reset()

        if (self.mode == "pause"):
            self.pauseMode()

        if (self.mode == "import"):
            self._import()

        if (self.mode == "export"):
            self._export()

    def changeCmdInTab(self, event):
        zone = self.whatZoneIsChoosed(event.x, event.y)
        if (zone is None):
            return

        y, x = zone//len(self.ordonnateur.colorTab[0]), zone%len(self.ordonnateur.colorTab[0])
        if (zone != -1 and zone != -2):
            color = self.ordonnateur.colorTab[y][x]

        else:
            color = Color(zone, zone)

        if (color == None):
            return

        self.ordonnateur.change_cmd(color)
        self.actualColor = color

        self.can.delete("cmd")

        graphicalTab = self.zone1.underZones[-1]
        cmdTab = self.ordonnateur.cmdTab
        l, h = len(cmdTab), len(cmdTab[0])
        i = -1
        for zone in range(h*l):
            if (zone%h == 0):
                i += 1

            txt = cmdTab[i][zone%h][1]
            txt = "" if (txt == "None") else txt
            self.can.create_text(graphicalTab.underZones[zone].getCenter()[0],
                                 graphicalTab.underZones[zone].getCenter()[1],
                                 text = "" if Color.notAColor(color) else txt,
                                 tags = ("cmd", "colorTab"))

        self.can.tag_bind("colorTab", "<Button-1>", self.changeCmdInTab)

    def colorZoneCodel(self, event):
        if ((self.mode == "single") or (self.mode == "recursive")):
            codel, z = self.whatCodeZoneIsChoosed(event.x, event.y)

            color = self.actualColor.convertColorToHexa()
            self.can.itemconfigure(codel.graphicZone, fill = color)
            codel.color = self.actualColor
            x = z%len(self.grille.grille[0])
            y = z//len(self.grille.grille[0])
            caseColor = self.grille.grille[y][x].getColor()
            self.grille.grille[y][x].change_couleur(self.actualColor)

            if (self.mode == "recursive"):
                self.cascadeColor(caseColor, self.grille.getCellule(y, x), [])

    def keyboardEvents(self, event):
        touche = event.keysym
        if touche == "Escape":
            self.quit()

    def quit(self, event = None):
        if (self.main != None):
            self.main.canQuit = True

            self.main.fen.deiconify()

            if not self.launched:
                self.main.programms[self.programmToChange].setGrid(self.grille)
                self.main.majCodeZone()
                self.fen.destroy()


            else:
                self.fen.destroy()
                self.main.programms[self.programmToChange].setStack(self.stack)
                self.main.programms[self.programmToChange].setOutput(self.output)
                self.main.launchGraphical(self.programmToChange + 1)

        else:
            self.fen.destroy()




########################################################################################
########################################################################################
########################################################################################
########################################################################################
##### Fonctions graphiques #############################################################
########################################################################################
########################################################################################
########################################################################################
########################################################################################
    def cascadeColor(self, color, origin, visites = []):
        visites.append(origin)
        origin.change_couleur(self.actualColor)

        actualColor = self.actualColor.convertColorToHexa()

        zone = self.zone2.underZones[0].underZones[origin.getX() + origin.getY()*len(self.grille.grille[0])]
        self.can.itemconfigure(zone.graphicZone, fill = actualColor)
        zone.color = actualColor

        for v in origin.voisins:
            if (v not in visites) and (Color.sameColor(color, v.getColor())):
                self.cascadeColor(color, v, visites)

    def makeCodeZone(self, codeZone):
        sx, sy = len(self.grille.getRow(0)), len(self.grille.getGrid())
        ssx, ssy = codeZone.getSizeX()/sx, codeZone.getSizeY()/sy
        for row in range(sy):
            for column in range(sx):
                codeZone.addZone(TouchableZone((column*ssx, row*ssy), (ssx, ssy),
                                self.grille.getCellule(row, column).getColor(),
                                               command = self.colorZoneCodel,
                                               tags = "codeZone"))

    def colorZone(self, zone, bg = -1):
        if (bg < 0):
            zone.creaZone(self.can)

        for i in range(len(zone.underZones)):
            self.colorZone(zone.underZones[i], bg - 1)

    def cleanGrid(self):
        g = self.grille.getGrid()
        for i in range(len(g)):
            for j in range(len(g[0])):
                self.grille.grille[i][j].color = Color.reconvertColor(g[i][j].getColor())

    def majCodelLector(self, codel):
        x, y = codel.getX(), codel.getY()
        zone = self.zone2.underZones[0].underZones[x + y*len(self.grille.grille[0])]
        cx, cy = zone.getCenter()[0], zone.getCenter()[1]

        self.can.delete("codelPointer")
        GraphicZone.arrow(self.can, zone, self.dp.direction_actuelle())


    def majOutput(self):
        self.can.delete("outputText")
        nbl = len(self.output.lines)
        if (self.firstLine >= nbl):
            return

        outputZone = self.zone3.underZones[2].underZones[-2]

        nbLines = len(self.output.lines)
        nbLinesForOutput = 10
        if ((nbl - self.firstLine) < 10):
            nbLinesForOutput = (nbl - self.firstLine)
            if (nbLinesForOutput < 0):
                nbLinesForOutput = 0

        elif (nbl < 10):
            nbLinesForOutput = nbl

        firstLine = self.firstLine

        nbCarPerLine = self.output.nbCarPerLine
        ncar = self.output.carNumber()

        for i in range(nbLinesForOutput):
            addy = i*outputZone.getSizeY()/10
            for j in range(nbCarPerLine):
                addx = j*outputZone.getSizeX()/nbCarPerLine
                self.can.create_text(
                    outputZone.getX() + addx + outputZone.getPax()/2,
                    outputZone.getY() + addy + outputZone.getPay()/2,
                    text = self.output.lines[firstLine + i][j],
                    tags = "outputText",
                    font = 'Georgia 15 bold')

    def majStack(self):
        self.can.delete("stackValue")
        stackZone = self.zone3.underZones[0].underZones[0]

        p1 = []
        i = 0
        while not (self.stack.empty() or i == (self.nbElementsInStack)):
            p1.append(self.stack.pop())

            zone = stackZone.underZones[i]
            self.can.create_text(zone.getX() + zone.getSizeX()/2,
                                 zone.getY() + zone.getSizeY()/2,
                                 text = str(p1[-1]), tags = "stackValue",
                                 font = 'Georgia 10 bold')
            i += 1

        for i in range(len(p1)):
            self.stack.empile(p1[-1 -i])

    def widgets(self):
        self.can = tk.Canvas(self.fen, bg = "light blue", height = self.size2,
                              width = self.size1)
        self.can.pack(side = tk.LEFT)

        #Création des zones et des sous-zones
        #Zone 1:
        #* Widgets pour dessiner
        #* Tableau des commandes
        self.zone1 = Zone((0, 0), (8*self.pax, 3*self.pay), COLOR5)

        #Bouton quitter
        if self.main == None:
            quitButton = TouchableZone((0, 0),
                                   (self.zone1.getPax()/4, self.zone1.getPax()/4),
                                   COLOR6,
                                   command = self.quit,
                                   tags = "quit")

        else:
            quitButton = Zone((-1, -1), (1, 1))

        self.zone1.addZone(quitButton)

        drawingWidgets = Zone((0, self.zone1.getEndY()/2 - 0.25*self.pay),
                              (2*self.pax, 0.5*self.pay))

        #Widgets pour dessiner
        nbWidgets = self.nbDrawingWidgets
        for i in range(nbWidgets):
            drawingWidgets.addZone(TouchableZone((i*drawingWidgets.getSizeX()/nbWidgets, 0),
                                                 (drawingWidgets.getSizeX()/nbWidgets,
                                                  drawingWidgets.getSizeY()),
                                                  COLOR7, command = self.chosenWidget,
                                                  tags = "widget"))

        self.zone1.addZone(drawingWidgets)


        #Changements de sets de couleur
        ox = drawingWidgets.getEndX() + self.zone1.getPax()
        size = len(self.ordonnateur.colorTab) - 2
        high = len(self.ordonnateur.colorTab[0]) + 1
        pas = (self.zone1.getEndX() - ox)/size
        pah = (self.zone1.getSizeY() - self.zone1.getPay())/high

        newSetsTab = Zone((ox, 0),
                         (self.zone1.getEndX() - ox,
                          self.zone1.getPay()),
                          "blue")

        self.zone1.addZone(newSetsTab)

        i = -1
        for couleur in self.ordonnateur.colorTab[:-2]:
            i += 1

            for j in range(3):  
                newSetsTab.addZone(TouchableZone((i*pas + j*(pas - pas/5)/3, 0),
                                                 ((pas - pas/5)/3, pah),
                                   Color(-5, j + 1).convertColorToHexa(),
                                   tags = "newSetsTabColor",
                                   command = self.changeSetColor))

        i = -1
        for couleur in self.ordonnateur.colorTab[:-2]:
            i += 1
            newSetsTab.addZone(TouchableZone((i*pas + pas - pas/5, 0), (pas/5, pah),
                               "#FFFFFF",
                               tags = "newSetsTabLst",
                               command = self.changeSetColor))
            

        #Tableau des couleurs
        colorTab = Zone((ox, self.zone1.getPay()),
                        (self.zone1.getEndX() - ox,
                         self.zone1.getSizeY() - self.zone1.getPay()),
                        "blue")

        self.zone1.addZone(colorTab)

        i = -1
        j = -1
        for couleur in self.ordonnateur.colorTab[:-2]:
            j = -1
            i += 1
            for teinte in couleur:
                j += 1
                colorTab.addZone(TouchableZone((i*pas, j*pah), (pas, pah),
                                 teinte.convertColorToHexa(),
                                 tags = "colorTab",
                                 command = self.changeCmdInTab))

        colorTab.addZone(TouchableZone((0, colorTab.getSizeY() - pah),
                                       (colorTab.getSizeX()/2, pah), "#FFFFFF",
                                       tags = "colorTab",
                                       command = self.changeCmdInTab))

        colorTab.addZone(TouchableZone((colorTab.getSizeX()/2, colorTab.getSizeY() - pah),
                                       (colorTab.getSizeX()/2, pah), "#000000",
                                        tags = "colorTab",
                                        command = self.changeCmdInTab))



        #Zone 2:
        #* Code
        self.zone2 = Zone((0, self.zone1.getEndY()),
                          (8*self.pax, self.size2 - self.zone1.getEndY()), COLOR8)

        #Zone de code
        ox = self.zone2.getPax()
        oy = self.zone2.getPay()
        codeZone = Zone((ox, oy), (self.zone2.getSizeX() - 2*self.zone2.getPax(),
                                   self.zone2.getSizeY() - 2*self.zone2.getPay()),
                        "orange")

        self.zone2.addZone(codeZone)

        #Lignes et colonnes du code selon la taille de la grille
        self.makeCodeZone(codeZone)
        self.codeZone = codeZone



        #Zone 3:
        #* Stack
        #* Input
        #* Output
        self.zone3 = Zone((self.zone2.getEndX(), 0),
                          (self.size1 - self.zone2.getEndX(), self.size2), "green")

        #Stack
        stackZone = Zone((0, 0),
                         (self.zone3.getSizeX(), 6*self.zone3.getPay()), COLOR9)
        self.zone3.addZone(stackZone)

        stack = Zone((stackZone.getSizeX()/4, 0),
                     (stackZone.getSizeX()/2, stackZone.getSizeY() - stackZone.getPay()),
                     "white")
        stackZone.addZone(stack)

        sy = stack.getSizeY()/self.nbElementsInStack
        for i in range(self.nbElementsInStack):
            stack.addZone(Zone((0, i*sy),
                               (stack.getSizeX(), sy),
                               "#DEFFDE"))

            self.can.create_text(stack.getX() + stack.getSizeX()/2,
                                  stack.getEndY() + stack.getPay()/2,
                                 text = "Stack", font = ('Georgia 15 bold'),
                                 tags = "stackValue")


        #Input
        inputZone = Zone((0, stackZone.getSizeY()),
                         (self.zone3.getSizeX(), 1*self.zone3.getPay()),
                         COLOR10)
        self.zone3.addZone(inputZone)
        validZone = TouchableZone((inputZone.getSizeX()/2 + inputZone.getPax()/2,
                                  5*inputZone.getPay()),
                                  (inputZone.getPax()*2,
                                  inputZone.getPay()*2),
                                  "white",
                                   tags = "validZone",
                                   command = self.validInput)
        inputZone.addZone(validZone)
        #self.can.tag_bind("validZone", "<Button-1>", self.validInput)


        #Output
        outputZone = Zone((0, inputZone.getEndY()),
                    (self.zone3.getSizeX(), self.zone3.getSizeY() - inputZone.getEndY()),
                          COLOR11)
        self.zone3.addZone(outputZone)

        ##Zone réelle de l'output
        outputZone.addZone(Zone((outputZone.getSizeX()/6, 2*outputZone.getPay()),
                                (outputZone.getSizeX()*(4/6), 7*outputZone.getPay()),
                                "white"))

        #Ajout de la scrollbar
        blankZone = outputZone.underZones[-1]
        outputZone.addZone(Zone((blankZone.getEndX() - outputZone.getX(),
                                 blankZone.getY() - outputZone.getY()),
                                (blankZone.getPax(), blankZone.getSizeY()),
                                "black"))

        #Ajout des boutons de la scrollBar avec Bind
        scroll = outputZone.underZones[-1]
        scroll.addZone(TouchableZone((0, 0),
                            (blankZone.getPax(), blankZone.getPax()),
                            "white", tags = "scrollBarUp",
                            command = lambda c : self.scroll(-1)))

        scroll.addZone(TouchableZone((0, blankZone.getSizeY() - blankZone.getPax()),
                            (blankZone.getPax(), blankZone.getPax()),
                             "white", tags = "scrollBarDown",
                             command = lambda c : self.scroll(1)))

        self.colorZone(self.zone1)
        self.colorZone(self.zone2)
        self.colorZone(self.zone3)


        #########################################################################
        #########################################################################
        #Textes et décorations supplémentaires
        #Zone 1: bouton quitter
        if self.main == None:
            GraphicZone.quitCross(self.can, quitButton)

        else:
            quitButton = self.can.create_text(35, 15,
                                             text = "Echap",
                                             font = ('Georgia 15 bold'),
                                             tags = "txtEchap")

        #Zone 1: widgets de dessin
        GraphicZone.pencil(self.can, drawingWidgets.underZones[0])
        self.can.tag_bind("pencil", "<Button-1>", self.chosenWidget)

        GraphicZone.bucket(self.can, drawingWidgets.underZones[1])
        self.can.tag_bind("bucket", "<Button-1>", self.chosenWidget)

        GraphicZone.start(self.can, drawingWidgets.underZones[2])
        self.can.tag_bind("start", "<Button-1>", self.chosenWidget)

        GraphicZone.reset(self.can, drawingWidgets.underZones[3])
        self.can.tag_bind("reset", "<Button-1>", self.chosenWidget)

        GraphicZone.stop(self.can, drawingWidgets.underZones[4])
        self.can.tag_bind("stop", "<Button-1>", self.chosenWidget)

        GraphicZone.pause(self.can, drawingWidgets.underZones[5])
        self.can.tag_bind("pause", "<Button-1>", self.chosenWidget)

        GraphicZone._import(self.can, drawingWidgets.underZones[6])
        self.can.tag_bind("import", "<Button-1>", self.chosenWidget)

        GraphicZone._export(self.can, drawingWidgets.underZones[7])
        self.can.tag_bind("export", "<Button-1>", self.chosenWidget)

        self.can.create_text(drawingWidgets.getCenter()[0],
                             drawingWidgets.getY() - self.zone1.getPay(),
                             text = "Widgets", font = ('Georgia 15'))

        #Zone 1: speed
        self.respeed = tk.Scale(self.fen, from_ = 1, to = 1000,
                                orient=tk.HORIZONTAL,
                                command = self.newSpeed)

        self.respeed.place(x = self.zone1.getX(),
                           y = self.zone1.getEndY() - self.zone1.getPay()*2)

        self.can.create_text(self.zone1.getX() + self.zone1.getPax()/2,
                             self.zone1.getEndY() - self.zone1.getPay()*2.5,
                             text = "MoveSpeed",
                             font = ('Gerogia 10'))

        #Zone 1: taille grille du code
        self.sizeCodeX = tk.Entry(self.fen, width = 3)
        self.sizeCodeX.insert(0, "5")
        self.sizeCodeY = tk.Entry(self.fen, width = 3)
        self.sizeCodeY.insert(0, "5")

        self.sizeCodeX.place(x = colorTab.getX() - colorTab.getPax()*3,
                             y = self.zone1.getEndY() - self.zone1.getPay())
        self.sizeCodeY.place(x = colorTab.getX() - colorTab.getPax()*3 + 60,
                             y = self.zone1.getEndY() - self.zone1.getPay())

        self.can.create_text(colorTab.getX() - colorTab.getPax()*3 + 15,
                             self.zone1.getEndY() - self.zone1.getPay()*1.5,
                             text = "Largeur", font = ('Georgia 10'))

        self.can.create_text(colorTab.getX() - colorTab.getPax()*3 + 75,
                             self.zone1.getEndY() - self.zone1.getPay()*1.5,
                             text = "Hauteur", font = ('Georgia 10'))


        #Zone 2: décorations
        codeZoneExtr = [(codeZone.getX(), codeZone.getY()),
                        (codeZone.getEndX(), codeZone.getY()),
                        (codeZone.getEndX(), codeZone.getEndY()),
                        (codeZone.getX(), codeZone.getEndY())]

        zone2Extr = [(self.zone2.getX(), self.zone2.getY()),
                     (self.zone2.getEndX(), self.zone2.getY()),
                     (self.zone2.getEndX(), self.zone2.getEndY()),
                     (self.zone2.getX(), self.zone2.getEndY())]

        scze = len(codeZoneExtr)
        w = 2
        c = "black"
        for i in range(len(codeZoneExtr)):
            self.can.create_line(codeZoneExtr[i][0], codeZoneExtr[i][1],
                                 zone2Extr[i][0], zone2Extr[i][1],
                                 fill = c, width = w,
                                 tags = "codeZone")

            self.can.create_line(codeZoneExtr[(i+1)%scze][0], codeZoneExtr[(i+1)%scze][1],
                                 zone2Extr[i][0], zone2Extr[i][1],
                                 fill = c, width = w,
                                 tags = "codeZone")

            self.can.create_line(codeZoneExtr[(i-1)%scze][0], codeZoneExtr[(i-1)%scze][1],
                                 zone2Extr[i][0], zone2Extr[i][1],
                                 fill = c, width = w,
                                 tags = "codeZone")


        #Zone 3: Stack
        self.can.create_text(stack.getX() + stack.getSizeX()/2,
                             stack.getEndY() + stack.getPay()/2,
                             text = "Stack", font = ('Georgia 15 bold'),
                             tags = "text")

        #Zone 3: Input
        self.can.create_text(inputZone.getX() + inputZone.getSizeX()/2,
                             inputZone.getY() + inputZone.getPay()*2,
                             text = "Input", tags = "text",
                             font = ('Georgia 15 bold'))

        self.inp = tk.Entry(self.fen, width = 4)
        self.inp.place(x = inputZone.getX() + inputZone.getSizeX()/2 - 15,
                       y = inputZone.getEndY() - 5*inputZone.getPay())

##        self.validInp = tk.Button(self.fen, text = "Valider", command = self.validInput)
##        self.validInp.place(x = inputZone.getX() + inputZone.getSizeX()/2 + 15,
##                              y = inputZone.getEndY() - 5*inputZone.getPay())
##

        self.can.create_text(validZone.getX() + validZone.getSizeX()/2,
                             validZone.getY() + validZone.getSizeY()/2,
                             text = "Valider",
                             tags = "validZone",
                             font = ('Georgia 10'))
        self.fen.bind("<Return>", self.validInput)


        #Zone 3: Output
        self.can.create_text(outputZone.getX() + outputZone.getSizeX()/2,
                             outputZone.getY() + outputZone.getPay(),
                             text = "Output", tags = "text",
                             font = ('Georgia 15 bold'))

        oz = outputZone.underZones[-2]
        self.can.create_text(oz.getX() + oz.getPax(),
                             oz.getY() + oz.getPay(),
                             text = self.output.output, tags = ("output", "outputText"),
                             font = ('Georgia 10 bold'))

        GraphicZone.arrow(self.can, outputZone.underZones[-1].underZones[0], (0, -1),
                           "scrollBarUp")
        GraphicZone.arrow(self.can, outputZone.underZones[-1].underZones[1], (0, 1),
                           "scrollBarDown")


if __name__ == "__main__":
    g = GraphicalInterpretor()
