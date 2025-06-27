

class Zone():
    def inZone(zone, x, y):
        return (zone.getX() < x < zone.getEndX() and zone.getY() < y < zone.getEndY())
    
    def __init__(self, origin, size, color = "red"):
        self.origin = origin
        self.size = size
        self.color = color
        self.graphicZone = None
        self.underZones = []

    def addZone(self, z):
        z.origin = (self.origin[0] + z.origin[0],
                     self.origin[1] + z.origin[1])
        self.underZones.append(z)

    def getX(self):
        return self.origin[0]

    def getY(self):
        return self.origin[1]

    def getSizeX(self):
        return self.size[0]

    def getSizeY(self):
        return self.size[1]

    def getEndX(self):
        return (self.getX() + self.getSizeX())

    def getEndY(self):
        return (self.getY() + self.getSizeY())

    def getPax(self):
        return self.getSizeX()/10

    def getPay(self):
        return self.getSizeY()/10

    def getCenter(self):
        return ((self.getEndX() + self.getX())/2, (self.getEndY() + self.getY())/2)

    def getCenterX(self):
        return (self.getEndX() + self.getX())/2

    def getCenterY(self):
        return (self.getEndY() + self.getY())/2

    def getColor(self):
        return self.color

    def creaZone(self, can, tags = "zone"):
        self.graphicZone = can.create_rectangle(self.getX(), self.getY(),
                             self.getEndX(), self.getEndY(),
                             fill = self.getColor(),
                             tags = tags)


class TouchableZone(Zone):
    def __init__(self, origin, size, color = "red", command = None, action = None, tags = ""):
        super().__init__(origin, size, color)
        self.command = command
        self.action = action
        self.tags = tags

    def creaZone(self, can, tags = "zone"):
        self.graphicZone = can.create_rectangle(self.getX(), self.getY(),
                             self.getEndX(), self.getEndY(),
                             fill = self.getColor(),
                             tags = self.tags)
        
        can.tag_bind(self.tags, "<Button-1>", self.command)
