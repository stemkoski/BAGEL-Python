import pygame, sys

from pygame.locals import * # contains constants like QUIT, K_UP, etc.

sys.path.append("src/")
from Texture import *
from Sprite import *
from Label  import *
from Group  import *
from ActionFactory import *
from Animation import *
from Game   import *
from random import * # contains randint function


class SpaceRocks(Game):

    def create(self):
        
        self.setTitle("Space Rocks")
        self.fpsDisplay = True

        space = Sprite()
        space.setTexture( Texture.load("assets/space-rocks/space.png") )
        space.setPosition(400,300)
        self.group.addEntity(space)

        self.spaceship = Sprite()
        self.spaceship.setTexture( Texture.load("assets/space-rocks/spaceship.png") )
        self.spaceship.setPosition(100,300)
        # physics values
        self.spaceship.setPhysics(100, 200, 10)
        self.spaceship.addAction( ActionFactory.wrapToScreen(800,600) )
        self.group.addEntity(self.spaceship)

        rockTexture = Texture.load("assets/space-rocks/rock.png")
        self.rockGroup = Group()
        self.group.addEntity( self.rockGroup )

        for n in range(6):
            rock = Sprite()
            x = random() * 400 + 300
            y = random() * 600
            rock.setPosition(x,y)
            rock.setTexture( rockTexture )
            rock.setPhysics(0,80,0)
            rock.physics.setSpeed(80)
            angle = random() * 360
            rock.angle = angle
            rock.physics.setMotionAngle( angle )
            rock.addAction( ActionFactory.wrapToScreen(800,600) )
            self.rockGroup.addEntity(rock)           

        self.laserTexture = Texture.load("assets/space-rocks/laser.png")
        self.laserGroup = Group()
        self.group.addEntity(self.laserGroup)
        
        self.explosionAnimation = Animation.load("assets/space-rocks/explosion.png", 6,6, 0.03, False)
        
        self.messageWin = Sprite()
        self.messageWin.setTexture( Texture.load("assets/space-rocks/message-win.png") )
        self.messageWin.setPosition(400,300)
        self.messageWin.opacity = 0
        self.messageWin.visible = False
        self.group.addEntity(self.messageWin)

    def update(self):

        if self.input.isKeyPressed(K_LEFT):
            self.spaceship.rotateBy(-2)
        if self.input.isKeyPressed(K_RIGHT):
            self.spaceship.rotateBy(2)
        if self.input.isKeyPressed(K_UP):
            self.spaceship.physics.accelerateAtAngle( self.spaceship.angle )

        if ( self.input.isKeyDown(K_SPACE) ):
            laser = Sprite()
            laser.setPosition( self.spaceship.x, self.spaceship.y )
            laser.setPhysics(0,400,0)
            laser.physics.setSpeed(400)
            laser.physics.setMotionAngle( self.spaceship.angle )
            laser.setTexture( self.laserTexture )
            laser.addAction( ActionFactory.wrapToScreen(800,600) )
            laser.addAction(
                ActionFactory.sequence(
                    ActionFactory.delay(1),
                    ActionFactory.fadeOut(0.5),
                    ActionFactory.remove()
                )
            )
            self.laserGroup.addEntity(laser)

        for laser in self.laserGroup.list():
            for rock in self.rockGroup.list():
                if ( laser.isOverlapping(rock) ):
                    laser.remove()
                    rock.remove()
                    explosion = Sprite()
                    explosion.setAnimation( self.explosionAnimation.clone() )
                    explosion.setPosition( rock.x, rock.y )
                    # remove after animation complete
                    explosion.addAction( 
                        ActionFactory.sequence(
                            ActionFactory.isAnimationFinished(),
                            ActionFactory.remove()
                        )
                    )
                    self.group.addEntity(explosion)

        if (self.rockGroup.count == 0 and not self.messageWin.visible):
            self.messageWin.visible = True
            self.messageWin.addAction( ActionFactory.fadeIn(2) )


###### end of class
            
game = SpaceRocks()
game.run()





