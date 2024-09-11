

class PointeurDirectionnel():
    def __init__(self, d = 0):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.pt = d

    def afficheEtat(self):
        print("Etat DP:")
        e = self.direction_actuelle()
        if (e == (1, 0)):
            print("-->")

        elif (e == (0, 1)):
            print("\\/")

        elif (e == (-1, 0)):
            print("<--")

        else:
            print("/\\")

        print()


    def roule(self, valeur = 1):
        self.pt += valeur
        self.pt %= 4

    def direction_actuelle(self):
        return self.directions[self.pt]

    def reinit(self):
        self.pt = 0

    def pointer(self, valeur = 1):
        self.roule(valeur)


class PointeurExtremite():
    def __init__(self, d = 0):
        self.directions = [1, -1]
        self.d = d

    def afficheEtat(self):
        print("Etat CC:")
        print("-->" if (self.direction_actuelle() == 1) else "<--")
        print()

    def reinit(self):
        self.pt = 0

    def roule(self, valeur = 1):
        self.d += valeur
        self.d %= 2

    def switch(self, valeur):
        self.roule(valeur)

    def direction_actuelle(self):
        return self.directions[self.d]

    def extremite_choisie(self, DP):
        if (DP.direction_actuelle()[0] == 1 and self.direction_actuelle() == -1):
            return ((0, 1))

        elif (DP.direction_actuelle()[0] == 1 and self.direction_actuelle() == 1):
            return ((0, -1))

        elif (DP.direction_actuelle()[1] == 1 and self.direction_actuelle() == -1):
            return ((1, 0))

        elif (DP.direction_actuelle()[1] == 1 and self.direction_actuelle() == 1):
            return ((-1, 0))

        elif (DP.direction_actuelle()[0] == -1 and self.direction_actuelle() == -1):
            return ((0, -1))

        elif (DP.direction_actuelle()[0] == -1 and self.direction_actuelle() == 1):
            return ((0, 1))

        elif (DP.direction_actuelle()[1] == -1 and self.direction_actuelle() == -1):
            return ((-1, 0))

        elif (DP.direction_actuelle()[1] == -1 and self.direction_actuelle() == 1):
            return ((1, 0))
