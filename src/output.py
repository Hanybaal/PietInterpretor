from random import randint

class OutPut():
    def __init__(self, nbCarPerLine = 10):
        self.output = ""
        self.nbCarPerLine = nbCarPerLine
        self.lines = [" "*self.nbCarPerLine]
        self.cursor = 0
##        self.nbTests = [[randint(0, 9) for i in range(self.nbCarPerLine)] for j in range(20)]
##        for i in range(len(self.nbTests)):
##            for j in range(len(self.nbTests[i])):
##                self.outNum(self.nbTests[i][j])

    def stack(self, v):            
        self.output += str(v)

        #Mise à jour des lignes pour l'interface graphique
        if ((self.cursor == self.nbCarPerLine) or (self.output[-1] == chr(10))):
            self.lines.append(" "*self.nbCarPerLine)
            self.cursor = 0         

        if (self.output[-1] != chr(10)):
            self.lines[-1] = self.lines[-1][:self.cursor] + str(v) + self.lines[-1][self.cursor+1:]
            self.cursor += 1
        
        #Réinitialisation de l'output
        self.reset_output()
        #self.affiche_output()

    def affiche_output(self):
        print(self.output)

    def nbReturn(self):
        n = 0
        for car in self.output:
            if (car == chr(10)):
                n += 1
        return n

    def reinit(self):
        self.output = ""

    def reset_output(self):
        pass

    def outChar(self, v : int):
        self.stack(chr(v))

    def outNum(self, v : int):
        self.stack(v)

    def carNumber(self):
        return len(self.output)

    def lineNumber(self, nbCarPerLine : int):
        n = 1
        cpt = nbCarPerLine

        for car in range(self.carNumber()):
            actualCar = self.output[car]
            if (cpt <= 1):
                n += 1
                cpt = nbCarPerLine
            
            elif (actualCar == chr(10)):
                cpt = nbCarPerLine
                n += 1

            else:
                cpt -= 1

        return n

    def getLines(self, nbCarPerLine : int):
        lines = []
        cpt = nbCarPerLine
        line = ""

        for car in range(self.carNumber()):
            actualCar = self.output[car]
            if (cpt <= 1):
                lines.append(line)
                line = actualCar
                cpt = nbCarPerLine
            
            elif (actualCar == chr(10)):
                cpt = 0

            else:
                #On ajoute un caractère à la ligne
                cpt -= 1
                if (actualCar != chr(10)):
                    line += actualCar

        return lines
