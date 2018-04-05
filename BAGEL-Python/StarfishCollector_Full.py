import pygame, sys, cProfile
from pygame.locals import * # contains constants like QUIT, K_UP, etc.
from random        import * # contains randint function

sys.path.append("src/")
from Action        import *
from ActionFactory import *
from Animation     import *
from Game          import *
from Group         import *
from Label         import *
from Sprite        import *
from Texture       import *

class StarfishCollector(Game):

    def create(self):
        
        self.setTitle("Starfish Collector")
        self.fpsDisplay = True
        
        ocean = Sprite()
        ocean.setTexture( Texture.load("assets/starfish-collector/water.jpg") )
        ocean.setPosition(400,300)
        self.group.addEntity(ocean)

        self.rock = Sprite()
        self.rock.setTexture( Texture.load("assets/starfish-collector/rock.png") )
        self.rock.setPosition(400,300)
        self.group.addEntity(self.rock)
        
        self.starfishGroup = Group()
        self.group.addEntity( self.starfishGroup )
        starfishTexture = Texture.load("assets/starfish-collector/starfish.png")
        for n in range(10):
            starfish = Sprite()
            x = random() * 800
            y = random() * 600
            starfish.setPosition(x,y)
            starfish.setTexture( starfishTexture )
            starfish.boundToScreen( 800, 600 )
            
            # reposition starfish if they overlap rock
            while ( starfish.isOverlapping(self.rock) ):
                x = random() * 800
                y = random() * 600
                starfish.setPosition(x,y)
                starfish.boundToScreen(800,600)

            # add a visual effect
            rotateSpeed = 20 + 40 * random()
            # starfish.addAction(  ActionFactory.forever( ActionFactory.rotateBy(rotateSpeed, 1) ) )
            
            self.starfishGroup.addEntity(starfish)

        self.turtle = Sprite(50,50)
        self.turtle.setTexture( Texture.load("assets/starfish-collector/turtle-down.png") )
        self.turtle.setPhysics(200, 100, 200)
        self.turtle.addAction( ActionFactory.boundToScreen(800,600) )
        self.group.addEntity(self.turtle)        

        fish = Sprite()
        fish.setPosition(750, 550)
        fishAnimation =	Animation.load("assets/starfish-collector/fish.png", 8,1, 0.15, True)
        fish.setAnimation(fishAnimation)
        fish.angle = -90
        fish.addAction(
            ActionFactory.forever(
                ActionFactory.sequence(
                    ActionFactory.moveBy(0,-500, 5),
                    ActionFactory.rotateBy(-180, 3),
                    ActionFactory.moveBy(0,500, 5),
                    ActionFactory.rotateBy(180, 3)
                )
            )
        )
        self.group.addEntity(fish)
		
        self.winMessage = Sprite()
        self.winMessage.setPosition(400,300)
        self.winMessage.setTexture( Texture.load("assets/starfish-collector/win-message.png") )
        self.winMessage.visible = False
        self.group.addEntity(self.winMessage)

        self.starfishLabel = Label()
        self.starfishLabel.loadFont("assets/starfish-collector/OpenSans.ttf", 48)
        self.starfishLabel.fontColor = (50,50,255)
        self.starfishLabel.setPosition( 400, 20 )
        self.starfishLabel.alignment = "CENTER"
        self.starfishLabel.text = "Hello, world!"
        self.group.addEntity(self.starfishLabel)

    def update(self):

        if self.input.isKeyPressed(K_LEFT):
            self.turtle.physics.accelerateAtAngle(180)
        if self.input.isKeyPressed(K_RIGHT):
            self.turtle.physics.accelerateAtAngle(0)
        if self.input.isKeyPressed(K_UP):
            self.turtle.physics.accelerateAtAngle(270)
        if self.input.isKeyPressed(K_DOWN):
            self.turtle.physics.accelerateAtAngle(90)            

        if self.input.isKeyDown(K_w):
            x = randint(0,700)
            y = randint(0,500)
            self.turtle.setPosition(x,y)

        self.turtle.preventOverlap(self.rock)
        
        for starfish in self.starfishGroup.list():
            if self.turtle.isOverlapping(starfish) and starfish.opacity == 1:
                starfish.actionList.clear()
                # need to reset angle because image rotation + transparency = bug
                starfish.angle = 0
                starfish.addAction(
                    ActionFactory.sequence(
                        ActionFactory.fadeOut(0.5),
                        ActionFactory.remove()
                    )
                )

        count = self.starfishGroup.count
        if (count > 0):
            self.starfishLabel.text = "Starfish left: " + str(count)
        else:
            self.starfishLabel.remove()
            self.winMessage.visible = True

        
game = StarfishCollector()
game.run()

# to check which parts require the most time to run, use a profiler:
# cProfile.run("game.run()")
