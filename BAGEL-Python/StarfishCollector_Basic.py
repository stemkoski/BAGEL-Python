import pygame, sys, cProfile
from pygame.locals import * # contains constants like QUIT, K_UP, etc.
from random        import * # contains randint function

sys.path.append("src/")
from Game          import *
from Group         import *
from Sprite        import *
from Texture       import *

class StarfishCollector(Game):

    def create(self):
        
        self.setTitle("Starfish Collector!")
        self.fpsDisplay = True
        
        ocean = Sprite()
        # for large images without transparency, jpg format is much smaller
        ocean.setTexture( Texture.load("assets/starfish-collector/water.jpg") )
        ocean.setPosition(400,300)
        self.group.addEntity(ocean)

        self.starfishGroup = Group()
        self.group.addEntity( self.starfishGroup )
        starfishTexture = Texture.load("assets/starfish-collector/starfish.png")
        for n in range(10):
            starfish = Sprite()
            x = random() * 800
            y = random() * 600
            starfish.setPosition(x,y)
            starfish.setTexture( starfishTexture )
            self.starfishGroup.addEntity(starfish)

        self.turtle = Sprite(50,50)
        self.turtle.setTexture( Texture.load("assets/starfish-collector/turtle-down.png") )
        self.group.addEntity(self.turtle)        

        self.winMessage = Sprite()
        self.winMessage.setPosition(400,300)
        self.winMessage.setTexture( Texture.load("assets/starfish-collector/win-message.png") )
        self.winMessage.visible = False
        self.group.addEntity(self.winMessage)

    def update(self):

        if self.input.isKeyPressed(K_LEFT):
            self.turtle.moveBy(-2, 0)
        if self.input.isKeyPressed(K_RIGHT):
            self.turtle.moveBy(2, 0)
        if self.input.isKeyPressed(K_UP):
            self.turtle.moveBy(0, -2)
        if self.input.isKeyPressed(K_DOWN):
            self.turtle.moveBy(0, 2)
           
        for starfish in self.starfishGroup.list():
            if self.turtle.isOverlapping(starfish):
                starfish.remove()

        if (self.starfishGroup.count == 0):
            self.winMessage.visible = True

        
game = StarfishCollector()
game.run()

# to check which parts require the most time to run, use a profiler:
# cProfile.run("game.run()")
