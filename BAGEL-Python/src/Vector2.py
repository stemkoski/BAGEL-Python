import math

class Vector2(object):

    def __init__(self, x=0, y=0):
        self.setValues(x,y)

    def __str__(self):
        return "[" + str(self.x) + " , " + str(self.y) + "]"

    def setValues(self, x, y):
        self.x = x
        self.y = y

    def addVector(self, other):
        self.x += other.x
        self.y += other.y

    def addValues(self, dx, dy):
        self.x += dx
        self.y += dy

    def multiply(self, scalar):
        self.x *= scalar
        self.y *= scalar

    def getLength(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def getAngle(self):
        # range: -180 to 180
        if (self.getLength() == 0):
            return 0
        else:
            return math.atan2(self.y, self.x) * 180/math.pi

    def setLength(self, length):
        angleDegrees = self.getAngle()
        self.x = length * math.cos(angleDegrees * math.pi/180)
        self.y = length * math.sin(angleDegrees * math.pi/180)

    def setAngle(self, angleDegrees):
        length = self.getLength()
        self.x = length * math.cos(angleDegrees * math.pi/180)
        self.y = length * math.sin(angleDegrees * math.pi/180)

    def compareTo(self, other):
        if (self.getLength() < other.getLength()):
            return -1
        elif (self.getLength() == other.getLength()):
            return 0
        else:
            return 1

