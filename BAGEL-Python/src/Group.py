from Entity import *

# manages a list of Entity objects

class Group(Entity):

    def __init__(self):
        self.entityList = []
        self.count = 0

    def addEntity(self, obj):
        obj.container = self
        self.entityList.append(obj)
        self.count += 1

    def removeEntity(self, obj):
        obj.container = None
        self.entityList.remove(obj)
        self.count -= 1

    # returns shallow copy of list
    def list(self):
        return self.entityList[:]

    def draw(self, displaySurface):
        for element in self.list():
            element.draw(displaySurface)
            
    def act(self, deltaTime):
        for element in self.list():
            element.act(deltaTime)

    
            
