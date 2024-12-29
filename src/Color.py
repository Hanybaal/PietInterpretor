

class Color():
    #Fonctions non rapportées aux couleurs de l'interpréteur
    def getRGBFromHexa(hexa : str):
        return tuple(int(hexa[i:i+2], 16) for i in (1, 3, 5))

    def getDarkerRGB(rgb : tuple, d : int):
        return tuple(0 if ((t + d) < 0) else 255 if ((t + d) > 255) else (t + d) for t in rgb)

    def getHexaFromRGB(rgb : tuple):
        return ("#{:02x}{:02x}{:02x}").format(rgb[0], rgb[1], rgb[2])

    #Fonctions liées à l'interpréteur en lui-même
    def notAColor(couleur):
        return ((couleur.getColor() < -9) and (couleur.getLuminosity() < 0) and
                (couleur.getColor() > 9))

    def reconvertColor(couleur):
        if (couleur.getColor() == -1):
            return Color(8, 0)

        elif (couleur.getColor() == -2):
            return Color(7, 0)

        return couleur

    def sameColor(c1, c2):
        return ((c1.getColor() == c2.getColor()) and (c1.getLuminosity() == c2.getLuminosity()))

    def convertHexaToColor(color : str) -> str:
        dico_convert = {"#FFC0C0" : "11",
                        "#FF0000" : "12",
                        "#C00000" : "13",
                        "#FFFFC0" : "21",
                        "#FFFF00" : "22",
                        "#C0C000" : "23",
                        "#C0FFC0" : "31",
                        "#00FF00" : "32",
                        "#00C000" : "33",
                        "#C0FFFF" : "41",
                        "#00FFFF" : "42",
                        "#00C0C0" : "43",
                        "#C0C0FF" : "51",
                        "#0000FF" : "52",
                        "#0000C0" : "53",
                        "#FFC0FF" : "61",
                        "#FF00FF" : "62",
                        "#C000C0" : "63",
                        "#FFFFFF" : "70",
                        "#000000" : "80",
                        "#FFFFFF" : "-2-2",
                        "#000000" : "-1-1",
                        "#DE9500" : "-31",
                        "#BD7500" : "-32",
                        "#9C5500" : "-33",
                        "#75CEB0" : "-41",
                        "#55ADB0" : "-42",
                        "#358CB0" : "-43",
                        "#FF00AA" : "-51",
                        "#CC0088" : "-52",
                        "#990055" : "-53"}
        return (dico_convert[str(color)])

    def __init__(self, couleur :  int, luminosite: int):
        self.color = couleur
        self.luminosity = luminosite
        self.hexa = self.convertColorToHexa()

    def __repr__(self) -> str:
        return (self.hexa)

    def convertColorToHexa(self) -> str:
        dico_convert = {"11" : "#FFC0C0",
                        "12" : "#FF0000",
                        "13" : "#C00000",
                        "21" : "#FFFFC0",
                        "22" : "#FFFF00",
                        "23" : "#C0C000",
                        "31" : "#C0FFC0",
                        "32" : "#00FF00",
                        "33" : "#00C000",
                        "41" : "#C0FFFF",
                        "42" : "#00FFFF",
                        "43" : "#00C0C0",
                        "51" : "#C0C0FF",
                        "52" : "#0000FF",
                        "53" : "#0000C0",
                        "61" : "#FFC0FF",
                        "62" : "#FF00FF",
                        "63" : "#C000C0",
                        "70" : "#FFFFFF",
                        "80" : "#000000",
                        "-2-2" : "#FFFFFF",
                        "-1-1" : "#000000",
                        "-31" : "#DE9500",
                        "-32" : "#BD7500",
                        "-33" : "#9C5500",
                        "-41" : "#75CEB0",
                        "-42" : "#55ADB0",
                        "-43" : "#358CB0",
                        "-51" : "#FF00AA",
                        "-52" : "#CC0088",
                        "-53" : "#990055"}
        return (dico_convert[str(self.color) + str(self.luminosity)])

    def getColor(self):
        return self.color

    def getLuminosity(self):
        return self.luminosity

    def isBlack(self):
        return (self.getColor() == 8)

    def isWhite(self):
        return (self.getColor() == 7)
