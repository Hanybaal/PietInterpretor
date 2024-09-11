

class Couleur():
    def notACouleur(couleur):
        return ((couleur.getCouleur() < 0) and (couleur.getLuminosite() < 0))

    def reconvertColor(couleur):
        if (couleur.getCouleur() == -1):
            return Couleur(8, 0)

        elif (couleur.getCouleur() == -2):
            return Couleur(7, 0)

        return couleur

    def sameColor(c1, c2):
        return ((c1.getCouleur() == c2.getCouleur()) and (c1.getLuminosite() == c2.getLuminosite()))
    
    def __init__(self, couleur :  int, luminosite: int):
        self.couleur = couleur
        self.luminosite = luminosite
        self.hexa = self.convertCouleurToHexa()

    def __repr__(self) -> str:
        return (self.hexa)

    def convertCouleurToHexa(self) -> str:
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
                        "-1-1" : "#000000"}
        return (dico_convert[str(self.couleur) + str(self.luminosite)])

    def getCouleur(self):
        return self.couleur

    def getLuminosite(self):
        return self.luminosite

    def isBlack(self):
        return (self.getCouleur() == 8)

    def isWhite(self):
        return (self.getCouleur() == 7)


        
