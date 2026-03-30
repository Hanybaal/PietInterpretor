

class Zone():
    def inZone(zone, x, y):
        return (zone.getX() < x < zone.getEndX() and zone.getY() < y < zone.getEndY())

    def getZoneByName(zone, name):
        if (zone.getName() == name):
            return zone

        for z in zone.getUnderZones():
            if (Zone.getZoneByName(z, name) != None):
                return Zone.getZoneByName(z, name)

        return None
    
    def __init__(self, origin, size, color = "red", name = "default"):
        self.origin = origin
        self.size = size
        self.color = color
        self.name = name
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

    def getName(self):
        return self.name

    def getUnderZones(self):
        return self.underZones

    def hasNameSet(self):
        return (self.getName() != "default")

    def creaZone(self, can, tags = "zone"):
        self.graphicZone = can.create_rectangle(self.getX(), self.getY(),
                             self.getEndX(), self.getEndY(),
                             fill = self.getColor(),
                             tags = tags)


class TouchableZone(Zone):
    def __init__(self, origin, size, color = "red", command = None, action = None, tags = "", name = ""):
        super().__init__(origin, size, color, name)
        self.command = command
        self.action = action
        self.tags = tags

    def creaZone(self, can, tags = "zone"):
        self.graphicZone = can.create_rectangle(self.getX(), self.getY(),
                             self.getEndX(), self.getEndY(),
                             fill = self.getColor(),
                             tags = self.tags)
        
        can.tag_bind(self.tags, "<Button-1>", self.command)
