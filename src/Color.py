import json

with open("../colors.json", "r", encoding="utf-8") as f:
    HEXTOCOL = json.load(f)
    print(HEXTOCOL)

COLTOHEX = {v: k for k, v in HEXTOCOL.items()}

ALLCOLORS = list(set([int(c[0:(len(c)-1)]) for c in HEXTOCOL.values()]))

class Color():
    #Les couleurs 7, 8, -1 et -2 restent blanc et noir, et ne comptent pas ici
    #allColors = [1, 2, 3, 4, 5, 6, -3, -4, -5, -6]
    allColors = ALLCOLORS
    print(allColors)
    allColors.remove(7)
    allColors.remove(8)

    def getLeftColors(colors):
        leftColors = []
        for color in Color.allColors:
            if (color not in colors):
                leftColors.append(color)
        return leftColors
    
    #Fonctions non rapportées aux couleurs de l'interpréteur
    def getRGBFromHexa(hexa : str):
        return tuple(int(hexa[i:i+2], 16) for i in (1, 3, 5))

    def getDarkerRGB(rgb : tuple, d : int):
        return tuple(0 if ((t + d) < 0) else 255 if ((t + d) > 255) else (t + d) for t in rgb)

    def getHexaFromRGB(rgb : tuple):
        return ("#{:02x}{:02x}{:02x}").format(rgb[0], rgb[1], rgb[2])

    #Fonctions liées à l'interpréteur en lui-même
    def notAColor(couleur):
        return ((couleur.getColor() < -50) and (couleur.getLuminosity() < 0) and
                (couleur.getColor() > 50))

    def notAColorfulColor(couleur):
        return (Color.notAColor(couleur) or couleur.isBlack() or couleur.isWhite())

    def reconvertColor(couleur):
        if (couleur.getColor() == -1):
            return Color(8, 0)

        elif (couleur.getColor() == -2):
            return Color(7, 0)

        return couleur

    def reconvertCol(couleur: int):
        if (couleur == -1):
            return 8

        elif (couleur == -2):
            return 7

        return couleur

    def reconvertLum(luminosity: int):
        if (luminosity == -1):
            return 0

        elif (luminosity == -2):
            return 0

        return luminosity

    def sameColor(c1, c2):
        return ((c1.getColor() == c2.getColor()) and (c1.getLuminosity() == c2.getLuminosity()))


    def convertHexaToColor(color: str) -> str:
        return HEXTOCOL[str(color)]

    def __init__(self, couleur :  int, luminosite: int):
        self.color = Color.reconvertCol(couleur)
        self.luminosity = Color.reconvertLum(luminosite)
        self.hexa = self.convertColorToHexa()

    def __repr__(self) -> str:
        return (self.hexa)

    def convertColorToHexa(self) -> str:
        return (COLTOHEX[str(self.color) + str(self.luminosity)])

    def getColor(self):
        return self.color

    def getLuminosity(self):
        return self.luminosity

    def getHexa(self):
        return self.hexa

    def setColor(self, c):
        self.color = c
        self.hexa = self.convertColorToHexa()

    def setLuminosity(self, l):
        self.luminosity = l
        self.hexa = self.convertColorToHexa()

    def isBlack(self):
        return ((self.getColor() == 8) or (self.getColor() == -1))

    def isWhite(self):
        return ((self.getColor() == 7) or (self.getColor() == -2))
