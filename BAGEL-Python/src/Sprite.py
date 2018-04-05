import pygame
import math

from Entity     import *
from Texture    import *
from Rectangle  import *
from Physics    import *

class Sprite(Entity):

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.texture = Texture()
        self.width = 0
        self.height = 0
        self.visible = True

        # collision
        self.boundary = Rectangle()

        # graphics
        self.angle = 0
        self.scale = 1 # not used
        self.opacity = 1
        self.mirrored = False
        self.flipped = False

        # physics
        self.physics = None

        # animation
        self.animation = None
        
        # actions
        self.actionList = []
        

    ###### basic methods
    
    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def moveBy(self, dx, dy):
        self.x += dx
        self.y += dy

    def setTexture(self, texture):
        self.texture = texture
        self.width   = texture.width
        self.height  = texture.height
        
    # override from GameObject class    
    def draw(self, displaySurface):

        if ( not self.visible ):
            return

        # if no modifications are made to the image, draw and return
        if ( not(self.opacity == 1) and not self.mirrored
             and not self.flipped and not(self.angle == 0) ):
            modifiedRect = self.texture.image.get_rect( center=(self.x, self.y) )    
            displaySurface.blit( self.texture.image, modifiedRect )
            return

        # if any modifications are made to the image, make a local copy
        modifiedImage = self.texture.image.copy()
            
        # mirror/flip, if needed
        if ( self.mirrored or self.flipped ):
            modifiedImage = pygame.transform.flip( modifiedImage, self.mirrored, self.flipped )
            
        # rotate, if needed
        # Note: rotating the image results in a larger image (larger bounding rectangle)
        #    which must be used as destination rectangle when blitting the image (for proper alignment)
        if ( not(self.angle == 0) ):
            modifiedImage = pygame.transform.rotozoom( modifiedImage, -self.angle, self.scale )

        # set opacity, if needed
        if ( not(self.opacity == 1) ):
            blendImage = pygame.Surface( (self.texture.width, self.texture.height), pygame.SRCALPHA)
            alpha = int(self.opacity * 255)
            blendImage.fill( (255, 255, 255, alpha) )
            modifiedImage.blit( blendImage, (0, 0), special_flags=pygame.BLEND_RGBA_MULT )
            #modifiedImage.set_alpha( int(self.opacity * 255) )
        
        modifiedRect = modifiedImage.get_rect( center=(self.x, self.y) )    
        displaySurface.blit( modifiedImage, modifiedRect )

    ###### collision methods

    def getBoundary(self):
        self.boundary.setValues(self.x - self.width/2, self.y - self.height/2, self.width, self.height)
        return self.boundary

    def isOverlapping(self, other):
        return self.getBoundary().overlaps( other.getBoundary() )

    def preventOverlap(self, other):
        if ( self.isOverlapping(other) ):
            mtv = self.getBoundary().getMinTranslationVector( other.getBoundary() )
            self.moveBy( -mtv.x, -mtv.y )

    ###### angle methods
    
    def rotateBy(self, da):
        self.angle += da
        
    def moveAtAngle(self, distance, angleDegrees):
        self.x += distance * math.cos(angleDegrees * math.pi/180)
        self.y += distance * math.sin(angleDegrees * math.pi/180)

    def moveForward(self, distance):
        self.moveAtAngle(distance, self.angle)
        
    ###### behavior methods

    def boundToScreen(self, screenWidth, screenHeight):
        if (self.x - self.width/2 < 0):
            self.x = self.width/2
        if (self.x + self.width/2 > screenWidth):
            self.x = screenWidth - self.width/2
        if (self.y - self.height/2 < 0):
            self.y = self.height/2
        if (self.y + self.height/2 > screenHeight):
            self.y = screenHeight - self.height/2

    def wrapToScreen(self, screenWidth, screenHeight):
        if (self.x + self.width/2 < 0):
            self.x = screenWidth + self.width/2
        if (self.x - self.width/2 > screenWidth):
            self.x = -self.width/2
        if (self.y + self.height/2 < 0):
            self.y = screenHeight + self.height/2
        if (self.y - self.height/2 > screenHeight):
            self.y = -self.height/2

    def isOnScreen(self, screenWidth, screenHeight):
        offScreen = (self.x + self.width/2 < 0) \
                    or (self.x - self.width/2 > screenWidth) \
                    or (self.y + self.height/2 < 0) \
                    or (self.y - self.height/2 > screenHeight)
        return (not offScreen)

    ###### physics methods

    def setPhysics(self, accValue, maxSpeed, decValue):
        self.physics = Physics(accValue, maxSpeed, decValue)

    # requires physics object to be initialized
    def bounceAgainst(self, other):
        if ( self.isOverlapping(other) ):
            mtv = self.getBoundary().getMinTranslationVector( other.getBoundary() )

            # prevent overlap
            self.moveBy(mtv.x, mtv.y);

            # assume surface perpendicular to displacement
            surfaceAngle = mtv.getAngle() + 90; 

            # adjust velocity
            self.physics.bounceAgainst(surfaceAngle);   
        
    ###### action methods

    def addAction(self, action):
        self.actionList.append(action)

    # override from Entity class
    def act(self, deltaTime):

        # update physics, position (based on velocity and acceleration)
        #   if it has been initialized for this sprite
        if ( not(self.physics == None) ):
            
            self.physics.positionVector.x = self.x
            self.physics.positionVector.y = self.y
            
            self.physics.update(deltaTime)
            
            self.x = self.physics.positionVector.x
            self.y = self.physics.positionVector.y
			
	# update animation, current texture
	#   if it has been initialized for this sprite
        if ( not(self.animation == None) ):
            self.animation.update(deltaTime)
            self.texture = self.animation.currentTexture

	# update all actions (in parallel, by default)
        actionListCopy = self.actionList[:]
        for action in actionListCopy:
            finished = action.apply(self, deltaTime)
            if (finished):
                self.actionList.remove(action)
    
    
    ###### animation methods

    def setAnimation(self, animation):
        self.animation = animation
        self.setTexture( animation.currentTexture )

