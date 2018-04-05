import pygame
from Vector2   import *

class Input(object):

    def __init__(self):
        self.keyDownList     = []
        self.keyPressedList  = []
        self.keyUpList       = []
        self.mouseButtonDown = False
        self.mouseButtonUp   = False
        
    def update(self, eventList):
        self.keyDownList = []
        self.keyUpList   = []
        self.mouseButtonDown = False
        self.mouseButtonUp   = False
        for event in eventList: # checks input events (discrete)
            if event.type == pygame.KEYDOWN:
                self.keyDownList.append( event.key )
                self.keyPressedList.append( event.key )
            if event.type == pygame.KEYUP:
                self.keyPressedList.remove( event.key )
                self.keyUpList.append( event.key )
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouseButtonDown = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.mouseButtonUp = True
            

    def isKeyDown(self, keyCode):
        return keyCode in self.keyDownList
    
    def isKeyUp(self, keyCode):
        return keyCode in self.keyUpList
    
    def isKeyPressed(self, keyCode):
        return keyCode in self.keyPressedList
    
    def getMousePosition(self):
        pos = pygame.mouse.get_pos()
        return Vector2( pos[0], pos[1] )

    def isMouseButtonUp(self):
        return self.mouseButtonUp

    def isMouseButtonDown(self):
        return self.mouseButtonDown

    def isClicked(self, sprite):
        pos = pygame.mouse.get_pos()
        return self.isMouseButtonDown() and sprite.getBoundary().contains(pos[0], pos[1])
