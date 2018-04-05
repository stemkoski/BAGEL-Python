import pygame
from Texture import *

class Animation(object):

    def __init__(self):
        self.currentTexture = None
        self.textureList = []
        self.frameDuration = 0.25
        self.loop = False
        self.elapsedTime = 0
        self.totalDuration = 0
        self.paused = False

    # updates elapsedTime and currentTexture
    def update(self, deltaTime):
        if (self.paused):
            return
        
        self.elapsedTime += deltaTime

        if (self.loop and self.elapsedTime > self.totalDuration):
            self.elapsedTime -= self.totalDuration

        textureIndex = int( self.elapsedTime / self.frameDuration) # int() rounds down for positive floats
        if ( textureIndex >= len(self.textureList) ):
            textureIndex = len(self.textureList) - 1
        self.currentTexture = self.textureList[textureIndex]

    def isFinished(self):
        return ((self.elapsedTime >= len(self.textureList) * self.frameDuration) and not self.loop)

    def clone(self):
        anim                = Animation()
        anim.textureList    = self.textureList
        anim.frameDuration  = self.frameDuration
        anim.loop           = self.loop
        anim.totalDuration  = self.totalDuration;
        anim.currentTexture = self.textureList[0];
        return anim

    @staticmethod
    def load(fileName, rows, cols, frameDuration, loop):
        anim = Animation()
        image = pygame.image.load(fileName)
        frameWidth = image.get_width()   / cols
        frameHeight = image.get_height() / rows
        
        for y in range(rows):
            for x in range(cols):
                subimage = pygame.Surface( (frameWidth, frameHeight), pygame.SRCALPHA )
                subimage.blit(image, (0, 0),
                              (x*frameWidth, y*frameHeight, frameWidth, frameHeight))
                texture = Texture()
                texture.image  = subimage
                texture.width  = frameWidth
                texture.height = frameHeight
                anim.textureList.append(texture)

        anim.frameDuration  = frameDuration
        anim.loop           = loop
        anim.totalDuration  = anim.frameDuration * len(anim.textureList)
        anim.currentTexture = anim.textureList[0]
        return anim



                
