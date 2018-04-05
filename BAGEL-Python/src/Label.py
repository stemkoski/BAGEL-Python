import pygame
from Entity import *

class Label(Entity):

    def __init__(self, fontName="Arial", fontSize=12):
        self.fontName = fontName
        self.fontSize = fontSize
        self.font = pygame.font.SysFont(fontName, fontSize)
        self.fontColor = (255,255,255)
        self.borderDraw = True
        self.borderSize = 1 # anything larger renders poorly
        self.borderColor = (0,0,0)      
        self.text = " "
        self.x = 0
        self.y = 0
        self.visible = True
        # values used for alignment
        self.alignment = "LEFT"
        self.alignValue = 0
        self.width  = 0
        self.height = 0
        
    def loadFont(self, fontFileName, fontSize=12):
        self.font = pygame.font.Font(fontFileName, fontSize)
        self.fontSize = fontSize

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    # override from Entity class
    def draw(self, displaySurface):

        if (not self.visible):
            return
        
        aa = True # antialiasing
        background = None
        textImage = self.font.render(self.text, aa, self.fontColor)

        # determine size of rendered text for alignment
        (self.width, self.height) = self.font.size(self.text)

        if (self.alignment == "LEFT"):
            self.alignValue = 0.0
        elif (self.alignment == "CENTER"):
            self.alignValue = 0.5
        elif (self.alignment == "RIGHT"):
            self.alignValue = 1.0
            
        textRect  = textImage.get_rect( topleft=(self.x - self.alignValue * self.width, self.y) )

        if (self.borderDraw):
            borderImage = self.font.render(self.text, aa, self.borderColor)
            displaySurface.blit( borderImage, textRect.move( self.borderSize,  self.borderSize) )
            displaySurface.blit( borderImage, textRect.move( self.borderSize, -self.borderSize) )
            displaySurface.blit( borderImage, textRect.move(-self.borderSize,  self.borderSize) )
            displaySurface.blit( borderImage, textRect.move(-self.borderSize, -self.borderSize) )
            
        displaySurface.blit( textImage, textRect )        
