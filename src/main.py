from Theme import *
from graphicInterpretor import *
from programm import *

class Main():
    def __init__(self):
        usr32 = ctypes.windll.user32
        self.size1 = usr32.GetSystemMetrics(0)
        self.size2 = usr32.GetSystemMetrics(1)
        self.pax = self.size1/10
        self.pay = self.size2/10

        self.fen = tk.Tk()

        self.fen.attributes('-fullscreen', True)
        self.fen.maxsize(self.size1, self.size2)
        self.fen.minsize(self.size1, self.size2)
        self.fen.bind('<Key>', self.keyboardEvents)

        self.programms = [] #Contient des objets Grille
        self.programmNames = []
        self.lastLaunchedProgrammIndex = 0

        self.canQuit = True
        self.lastCode = None

        self.widgets()
        self.menu()

        self.fen.mainloop()

    def launch(self):
        if (len(self.programms) <= 1):
            return
        
        #On réinitialise les outputs et les stacks
        for prog in range(len(self.programms) - 1):
            self.programms[prog].setStack(Pile())
            self.programms[prog].setOutput(OutPut())
        
        i = None
        for prog in range(len(self.programms) - 1):
            i = InterpreteurPiet(grille = self.programms[prog].getGrid(),
                             stack = self.lastSharedStack(),
                             output = self.lastSharedOutput())

            i.lecture(i.grille, i.grille.getCellule(0, 0), 0, True)
            self.programms[prog].setStack(i.stack)
            self.programms[prog].setOutput(i.output)

        print("Rendu final:")
        i.affichePile()
        print()
        print("Output:")
        i.output.affiche_output()

    def rename(self, n):
        self.programms[self.lastLaunchedProgrammIndex].name = n
        self.can.itemconfigure(self.programmNames[self.lastLaunchedProgrammIndex],
                               text = n)
        self.can.update()

    def getInterpretor(self, event):
        codesZone = self.zone2.underZones[0]
        x, y = event.x, event.y
        indice = 0
        while (not Zone.inZone(codesZone.underZones[indice], x, y)):
            indice += 1
        self.lastCode = indice

        self.canQuit = False

        self.lastLaunchedProgrammIndex = indice
        i = GraphicalInterpretor(main = self, grille = self.programms[indice].getGrid(),
                                 ptc = indice)

        self.programms[indice].name = i.programmName


    def menu(self):
        pass

    def widgets(self):
        self.can = tk.Canvas(self.fen, bg = "light blue", height = self.size2,
                              width = self.size1)
        self.can.pack(side = tk.LEFT)


        self.zone1 = Zone((0, 0), (self.size1, self.pay*4), COLOR1)
        self.zone2 = Zone((0, self.zone1.getEndY()),
                          (self.size1, self.size2 - self.zone1.getEndY()), COLOR2)

        #Zone 1:
        #* Bouton quitter

        #Fond d'écran
        rapport = max(self.zone1.getSizeX(), self.zone1.getSizeY())/min(self.zone1.getSizeX(), self.zone1.getSizeY())

        p2 = 10
        p1 = int(p2*rapport)

        for i in range(p1):
            for j in range(p2):
                self.zone1.addZone(
                    Zone((self.zone1.getX() + self.zone1.getSizeX()/p1*i,
                          self.zone1.getY() + self.zone1.getSizeY()/p2*j),
                    (self.zone1.getSizeX()/p1, self.zone1.getSizeY()/p2),
                    color = SET1[randint(0, len(SET1) - 1)]))
        

        #Bouton quitter
        quitButton = TouchableZone((0, 0),
                                   (self.zone1.getPax()/4, self.zone1.getPax()/4),
                                   "red",
                                   command = self.quit,
                                   tags = ("quit"))

        presentationZone = Zone((self.zone1.getCenter()[0]/2, self.zone1.getCenter()[1]/2),
                                (self.zone1.getSizeX()/2, self.zone1.getSizeY()/2),
                                color = COLOR3)
        
        self.zone1.addZone(quitButton)
        self.zone1.addZone(presentationZone)        


        #Zone 2:
        #* Zone avec les programmes
        zoneCodes = Zone((self.zone2.getPax()*2, self.zone2.getPay()*0.5),
                         (self.zone2.getPax()*6, self.zone2.getPay()*9),
                         COLOR4)
        self.zone2.addZone(zoneCodes)

        self.colorZone(self.zone1)
        self.colorZone(self.zone2)


        #Décorations
        ZoneGraphism.quitCross(self.can, quitButton)
        self.can.create_text(presentationZone.getX() + presentationZone.getSizeX()/2,
                             presentationZone.getY() + presentationZone.getPay()/2 +
                             presentationZone.getPay(),
                             text = "Bienvenue au compilateur Piet!!",
                             font = ('Georgia 15 bold'),
                             tags = "stackValue")

        self.can.create_text(presentationZone.getX() + presentationZone.getSizeX()/2,
                             presentationZone.getY() + presentationZone.getPay()/2 +
                             presentationZone.getPay()*4,
                             text = "***  La led du dessus sert à enregistrer le stack  ***",
                             font = ('Georgia 15 bold'),
                             tags = "stackValue")

        self.can.create_text(presentationZone.getX() + presentationZone.getSizeX()/2,
                             presentationZone.getY() + presentationZone.getPay()/2 +
                             presentationZone.getPay()*6,
                             text = "***  La led du dessous sert à enregistrer l'output  ***",
                             font = ('Georgia 15 bold'),
                             tags = "stackValue")
        

        #Zone 2: first programm
        self.addProgZone()

        self.launchButton = tk.Button(self.fen, text = "Lancer", command = self.launch)
        self.launchButton.place(x = presentationZone.getX() + presentationZone.getSizeX()/2,
                                y = presentationZone.getEndY() + presentationZone.getPay())

##       #Zone 2: change the theme color
##        self.changeTheme = tk.Scale(self.fen, from_ = 1, to = 255,
##                                orient=tk.HORIZONTAL,
##                                command = self.darkerTheme)
##
##        self.changeTheme.place(x = self.zone1.getX(),
##                           y = self.zone1.getEndY() - self.zone1.getPay()*2)

    def darkerTheme(self, event):
        print(self.changeTheme.get())
        

    def addProgZone(self, event = None):
        nbProgrammsPerLine = 8
        nbLines = 8
        nbCodes = len(self.programms)
        if (nbCodes > (nbLines*nbProgrammsPerLine - 1)):
            return

        zoneCodes = self.zone2.underZones[0]

        x = nbCodes%nbProgrammsPerLine
        y = nbCodes//nbProgrammsPerLine
        spacex = (zoneCodes.getSizeX() - zoneCodes.getPax()*nbProgrammsPerLine)
        spacex *= (0 if x == 0 else x)/nbProgrammsPerLine
        spacey = (zoneCodes.getSizeY() - zoneCodes.getPay()*nbLines)
        spacey *= (0 if y == 0 else y)/nbLines

        #self.can.delete("addProgZone")
        self.can.delete("plus")
        progZone = TouchableZone((x*zoneCodes.getPax() + spacex,
                                  y*zoneCodes.getPay() + spacey),
                                 (zoneCodes.getPax(), zoneCodes.getPay()),
                                 "orange",
                                 command = self.addProgZone,
                                 tags = "addProgZone")
        zoneCodes.addZone(progZone)
        progZone.creaZone(self.can)

        self.programms.append(Programm())
        #if (len(self.programms) == 1):
        if (True):
            self.programms[-1].blankInit()

        else:
            lastProgramm = self.programms[-1]
            lastProgramm.setStack(self.lastSharedStack())
            lastProgramm.setOutput(self.lastSharedOutput())
            lastProgramm.setGrid(Grille(5, 5))

        lastProgramm = self.programms[-1]

        self.makeCodeZone(progZone)

        ZoneGraphism.plus(self.can, progZone)
        f1, f2 = ZoneGraphism.feux(self.can, progZone)
        lastProgramm.setFires(f1, f2)
        self.can.tag_bind("plus", "<Button-1>", self.addProgZone)
        self.can.tag_bind(f1, "<Button-1>",
                          lambda c : lastProgramm.changeStackState(self.can))
        self.can.tag_bind(f2, "<Button-1>",
                          lambda c : lastProgramm.changeOutputState(self.can))

        if (len(self.programms) > 0):
            cz = progZone.underZones[-1]
            self.programmNames.append(
                self.can.create_text(cz.getCenter()[0], cz.getEndY() + cz.getPay()*1.2,
                            text = self.programms[-1].name,
                            font = ('Georgia 7 bold'),
                            tags = "stackValue"))

    def majCodeZone(self):
        indexProgramm = self.lastCode
        p = self.programms[indexProgramm]
        grid = p.getGrid()
        z = self.zone2.underZones[0].underZones[indexProgramm]
        z.underZones = []
        sx, sy = len(grid.getRow(0)), len(grid.getGrille())
        ssx, ssy = z.getSizeX()/sx, z.getSizeY()/sy

        #Met la grille à jour dans le compilateur de codes de sorte qu'à l'appui
        #L'interpréteur se lance
        for i in range(len(grid.getGrille())):
            for j in range(len(grid.getGrille()[0])):
                color = grid.getCellule(i, j).getCouleur().convertCouleurToHexa()
                z.addZone(TouchableZone((j*ssx, i*ssy), (ssx, ssy),
                                                color,
                                                tags = "editor",
                                                command = self.getInterpretor))
                z.underZones[-1].creaZone(self.can)
        z.underZones[-1].creaZone(self.can)
##                toModify = z.underZones[j + i*len(grid.getGrille()[0])].graphicZone
##                self.can.itemconfigure(toModify, fill = color)

    def blankProgramm(self):
        return Grille(5, 5)

    def makeCodeZone(self, codeZone, g = None):
        if (g == None):
            g = self.blankProgramm()
        sx, sy = len(g.getRow(0)), len(g.getGrille())
        ssx, ssy = codeZone.getSizeX()/sx, codeZone.getSizeY()/sy
        for row in range(sy):
            for column in range(sx):
                codeZone.addZone(TouchableZone((column*ssx, row*ssy), (ssx, ssy),
                                                Couleur(7, 0),
                                        tags = "editor",
                                        command = self.getInterpretor))

                codeZone.underZones[-1].creaZone(self.can)
        codeZone.addZone(TouchableZone((0, 0),
                                       (codeZone.getSizeX(), codeZone.getSizeY()),
                                       "light goldenrod", tags = "plus",
                                       command = self.addProgZone))
        codeZone.underZones[-1].creaZone(self.can)


    def lastSharedStack(self):
        i = len(self.programms) - 2
        while not (i == -1):
            actualProgramm = self.programms[i]

            #On fait une copy deep de la pile pour éviter que
            #Si p2 hérite de p1, elle n'influe pas sur la pile de p1
            if (actualProgramm.sharingStack()):
                s1 = actualProgramm.getStack()
                newStack = Pile()
                newStack.pile = list(s1.pile)
                newStack.hauteur = s1.hauteur
                return newStack
            i -= 1

        return Pile()

    def lastSharedOutput(self):
        i = len(self.programms) - 2
        while not (i == -1):
            actualProgramm = self.programms[i]
            if (actualProgramm.sharingOutput()):
                o1 = actualProgramm.getOutput()
                newOutput = OutPut()
                newOutput.output = str(o1.output)
                return newOutput
            i -= 1

        return OutPut()


    def changeStateShare(self, event):
        x = event.x
        y = event.y
        item_id = event.widget.find_closest(x, y)[0]

        fill_color = event.widget.itemcget(item_id, "fill")
        newFill = "green" if (fill_color == "red") else "red"

        # Changez la couleur de l'item sur lequel vous avez cliqué
        event.widget.itemconfigure(item_id, fill = newFill)

    def colorZone(self, zone, bg = -1):
        if (bg < 0):
            zone.creaZone(self.can)

        for i in range(len(zone.underZones)):
            self.colorZone(zone.underZones[i], bg - 1)


    def keyboardEvents(self, event):
        touche = event.keysym
        if touche == "Escape":
            self.quit()

    def quit(self, event = None):
        if self.canQuit:
            self.fen.destroy()


    def clean(self):
        self.can.delete("all")


if __name__ == "__main__":
    g = Main()
