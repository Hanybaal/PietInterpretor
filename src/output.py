

class OutPut():
    def __init__(self):
        self.output = ""

    def stack(self, v):
        self.output += str(v)
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

    def lineNumber(self, nbCarPerLine):
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
