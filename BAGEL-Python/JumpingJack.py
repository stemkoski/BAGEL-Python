import pygame, sys, cProfile
from pygame.locals import * # contains constants like QUIT, K_UP, etc.
from random        import * # contains randint function

sys.path.append("src/")
from Action          import *
from ActionFactory   import *
from Animation       import *
from Game            import *
from Group           import *
from Label           import *
from PlatformPhysics import *
from Sprite          import *
from Texture         import *
from TileMap         import *

class JumpingJack(Game):

    def create(self):

        self.setWindowSize( 15*64, 10*64 )
        self.setTitle("Jumping Jack")
        self.fpsDisplay = True
        
        background = Sprite()
        background.setTexture( Texture.load("assets/jumping-jack/background.jpg") )
        background.setPosition(480,320)
        self.group.addEntity(background)

        self.worldMap = TileMap(10,15, 64,64)
        mapData = [
                "_______________",
                "_______________",
                "_______________",
                "C_____________A",
                "D_____________D",
                "D__B__AC______D",
                "D________ABC__D",
                "D_J_____AD___AD",
                "D____________DD",
                "DBBBBBBBBBBBBDD"  ]
        mapDataSymbolArray  = ["A", "B", "C", "D"]
        tileImageIndexArray = [1, 2, 3, 0]
        self.worldMap.loadMapData( mapData, mapDataSymbolArray, tileImageIndexArray )
        self.worldMap.loadTilesetImage("assets/jumping-jack/tileset.png")
        self.group.addEntity(self.worldMap);

        self.jack = Sprite()
        pos = self.worldMap.getSymbolPositionList("J")[0]
        self.jack.setPosition( pos.x, pos.y );
        self.jack.addAction( ActionFactory.boundToScreen(960,640) )

        self.jack.physics = PlatformPhysics(512,128,512, 450,700,1000)

        self.animWalk  = Animation.load( "assets/jumping-jack/walk.png",  1, 4, 0.15, True )
        self.animStand = Animation.load( "assets/jumping-jack/stand.png", 1, 1, 1.00, True )
        self.animJump  = Animation.load( "assets/jumping-jack/jump.png",  1, 1, 1.00, True )
        self.jack.setAnimation(self.animWalk)

        self.group.addEntity(self.jack)

    def update(self):
        
        # walking
        if ( self.input.isKeyPressed(K_RIGHT) ):
            self.jack.physics.accelerateAtAngle(0)
        if ( self.input.isKeyPressed(K_LEFT) ):
            self.jack.physics.accelerateAtAngle(180)

        # collision detection
        self.worldMap.preventSpriteOverlap( self.jack )

        # check if on ground
        self.jack.moveBy(0,2)
        onGround = self.worldMap.checkSpriteOverlap(self.jack)
        self.jack.moveBy(0,-2)

        # jump
        if ( self.input.isKeyDown(K_SPACE) and onGround ):
            self.jack.physics.jump()

        # manage animations
        if (onGround):
            if ( self.jack.physics.velocityVector.x == 0 ):
                self.jack.setAnimation(self.animStand)
            else:
                self.jack.setAnimation(self.animWalk)
        else:
            self.jack.setAnimation(self.animJump)

        # face right/left by mirroring image
        if ( self.jack.physics.velocityVector.x > 0 ): 
            self.jack.mirrored = False
        if ( self.jack.physics.velocityVector.x < 0 ):
            self.jack.mirrored = True

  
game = JumpingJack()
game.run()

