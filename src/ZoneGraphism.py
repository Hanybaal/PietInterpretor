from math import *

class ZoneGraphism():
    def dataExtraction(zone):
        return (zone.getCenter()[0], zone.getCenter()[1], zone.getPax(),
                zone.getPay(), zone.getX(), zone.getY(), zone.getEndX(), zone.getEndY())

    def quitCross(can, zone):
        cx, cy, px, py, x, y, ex, ey = ZoneGraphism.dataExtraction(zone)

        can.create_line(x + 2*px, y + 2*py,
                        ex - 2*px, ey - 2*py,
                        fill = "black", width = 2, tags = "quit")

        can.create_line(x + 2*px, ey - 2*py,
                        ex - 2*px, y + 2*py,
                        fill = "black", width = 2, tags = "quit")


    def pencil(can, zone):
        cx, cy, px, py, x, y, ex, ey = ZoneGraphism.dataExtraction(zone)

        can.create_polygon(cx, y + py,
                           cx + 2*px, y + 4*py,
                           cx + 2*px, ey - py,
                           cx - 2*px, ey - py,
                           cx - 2*px, y + 4*py,
                           fill = "green", outline = "black",
                           tags = "pencil")

        for i in range(4):
            can.create_line(cx - 2*px + (i + 1)*4/5*px, y + 4*py,
                            cx - 2*px + (i + 1)*4/5*px, ey - py,
                            tags = "pencil")

    def bucket(can, zone):
        cx, cy, px, py, x, y, ex, ey = ZoneGraphism.dataExtraction(zone)

        can.create_polygon(cx + 1.5*px + 2*px, y + 2*py,
                           cx + 1.5*px, y + 4*py,
                           cx + 1.5*px, ey - 2*py,
                           cx - 2.5*px, ey - 2*py,
                           cx - 2.5*px, y + 2*py,
                           fill = "pale green", outline = "black",
                           tags = "bucket")

    def start(can, zone):
        cx, cy, px, py, x, y, ex, ey = ZoneGraphism.dataExtraction(zone)

        can.create_polygon(x + 2*px, y + 2*py,
                           ex - 2*px, cy,
                           x + 2*px, ey - 2*py,
                           fill = "firebrick1", outline = "black",
                           tags = "start")

    def arrow(can, zone, direction):
        cx, cy, px, py, x, y, ex, ey = ZoneGraphism.dataExtraction(zone)
        dx, dy = direction[0], direction[1]

        #Flemme de faire tous les calculs
        if (dx != 0):
            can.create_polygon(cx - 2*px*dx, cy - py/2,
                               cx + px*dx, cy - py/2,
                               cx + px*dx, cy - py,
                               cx + 2*px*dx, cy,
                               cx + px*dx, cy + py,
                               cx + px*dx, cy + py/2,
                               cx - 2*px*dx, cy + py/2,
                               fill = "DarkOrange1", tags = "codelPointer",
                               outline = "black", width = 1)

        else:
            can.create_polygon(cx - px/2, cy - 2*py*dy,
                               cx - px/2, cy + py*dy,
                               cx - px, cy + py*dy,
                               cx, cy + 2*py*dy,
                               cx + px, cy + py*dy,
                               cx + px/2, cy + py*dy,
                               cx + px/2, cy - 2*py*dy,
                               fill = "DarkOrange1", tags = "codelPointer",
                               outline = "black", width = 1)

    def reset(can, zone):
        cx, cy, px, py, x, y, ex, ey = ZoneGraphism.dataExtraction(zone)

        can.create_line(cx, cy + 2*py,
                        cx + 2*px, cy + 2*py,
                        cx + 2*px, cy - 2*py,
                        cx - 2*px, cy - 2*py,
                        width = 2, tags = "reset")

        can.create_line(cx - 2*px + px, cy - 2*py - py,
                        cx - 2*px, cy - 2*py,
                        cx - 2*px + px, cy - 2*py + py,
                        width = 2, tags = "reset")

    def stop(can, zone):
        cx, cy, px, py, x, y, ex, ey = ZoneGraphism.dataExtraction(zone)
        coef = 3

        can.create_rectangle(x + coef*px, y + coef*py,
                             ex - coef*px, ey - coef*py,
                             fill = "#FF0000", outline = "#000000",
                             tags = "stop")

    def pause(can, zone):
        cx, cy, px, py, x, y, ex, ey = ZoneGraphism.dataExtraction(zone)
        coef = 3

        can.create_oval(x + coef*px, y + coef*py,
                        ex - coef*px, ey - coef*py,
                        fill = "#FF0000", outline = "#000000",
                        tags = "pause")

    def _import(can, zone):
        cx, cy, px, py, x, y, ex, ey = ZoneGraphism.dataExtraction(zone)

        taille = 2.5

        can.create_line(cx - px, y + taille*py,
                        x + taille*px, y + taille*py,
                        x + taille*px, ey - taille*py,
                        ex - taille*px, ey - taille*py,
                        ex - taille*px, y + taille*py,
                        cx + px, y + taille*py,
                        width = 2, tags = "import")

        can.create_line(cx, y + py,
                        cx, ey - 3.5*py,
                        width = 2, tags = "import")

        can.create_polygon(cx - px, cy,
                           cx, ey - 3.5*py,
                           cx + px, cy,
                           width = 2, tags = "import")


    def _export(can, zone):
        cx, cy, px, py, x, y, ex, ey = ZoneGraphism.dataExtraction(zone)

        taille = 2.5

        can.create_line(cx - px, y + taille*py,
                        x + taille*px, y + taille*py,
                        x + taille*px, ey - taille*py,
                        ex - taille*px, ey - taille*py,
                        ex - taille*px, y + taille*py,
                        cx + px, y + taille*py,
                        width = 2, tags = "export")

        can.create_line(cx, y + 2*py,
                        cx, ey - 3.5*py,
                        width = 2, tags = "export")

        can.create_polygon(cx - px, y + 3.5*py,
                           cx, y + 2*py,
                           cx + px, y + 3.5*py,
                           width = 2, tags = "export")

    def plus(can, zone):
        cx, cy, px, py, x, y, ex, ey = ZoneGraphism.dataExtraction(zone)

        size = 3
        p = min(px, py)

        can.create_line(cx, cy - size*p,
                        cx, cy + size*p,
                        width = 3, tags = "plus")

        can.create_line(cx - size*p, cy,
                        cx + size*p, cy,
                        width = 3, tags = "plus")

    def feux(can, zone):
        cx, cy, px, py, x, y, ex, ey = ZoneGraphism.dataExtraction(zone)

        size = 3
        p = min(px, py)
        f1 = can.create_oval(ex, y,
                        ex + size*p, y + size*p,
                        fill = "red", tags = "fireStack")

        f2 = can.create_oval(ex, ey,
                        ex + size*p, ey - size*p,
                        fill = "red", tags = "fireOutput")

        return (f1, f2)
