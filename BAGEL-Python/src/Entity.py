
class Entity(object):

    def __init__(self):
        self.container = None

    def remove(self):
        if (self.container is not None):
            self.container.removeEntity(self)

    def draw(self, displaySurface):
        pass

    def act(self, deltaTime):
        pass
    

    
