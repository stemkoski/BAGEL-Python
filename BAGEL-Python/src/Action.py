
class Action(object):

    def __init__(self, f=None):
        self.totalTime = 0
        self.actFunction = f

    def apply(self, target, deltaTime):
        self.totalTime += deltaTime
        return self.actFunction(target, deltaTime, self.totalTime)
    
    def reset(self):
        self.totalTime = 0
