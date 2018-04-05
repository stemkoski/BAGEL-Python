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
from TileMap       import *

class MapExplorer(Game):

    def create(self):

        self.setWindowSize( 12*64, 10*64 )
        self.setTitle("Map Explorer")
        self.fpsDisplay = True
        
        ocean = Sprite()
        ocean.setTexture( Texture.load("assets/starfish-collector/water.jpg") )
        ocean.setPosition(400,300)
        self.group.addEntity(ocean)

        self.map = TileMap(10,12, 64,64)
        
        mapData = [
                "AAAAAAAAAAAA",
                "AT_____C___A",
                "A_BBB______A",
                "A__BBB__C__A",
                "A__________A",
                "A_C__BB__C_A",
                "A____BBB___A",
                "A__C__B___CA",
                "A_______C__A",
                "AAAAAAAAAAAA"  ]
        
        mapDataSymbolArray  = ["A", "B", "C"]
        tileImageIndexArray = [4, 14, 2]
        self.map.loadMapData( mapData, mapDataSymbolArray, tileImageIndexArray );
        self.map.loadTilesetImage("assets/map-explorer/tileset.png")
        self.group.addEntity(self.map);

        self.turtle = Sprite()
        self.turtle.setTexture( Texture.load("assets/map-explorer/turtle.png") )
        pos = self.map.getSymbolPositionList("T")[0]
        self.turtle.setPosition( pos.x, pos.y )
        self.group.addEntity(self.turtle)
        self.turtle.setPhysics(512,64,512)
        
    def update(self):
        if ( self.input.isKeyPressed(K_UP) ):
            self.turtle.physics.accelerateAtAngle(270)
        if ( self.input.isKeyPressed(K_DOWN) ):
            self.turtle.physics.accelerateAtAngle(90)
        if ( self.input.isKeyPressed(K_RIGHT) ):
            self.turtle.physics.accelerateAtAngle(0)
        if ( self.input.isKeyPressed(K_LEFT) ):
            self.turtle.physics.accelerateAtAngle(180)

        self.map.preventSpriteOverlap( self.turtle )
        
        motionAngle = self.turtle.physics.getMotionAngle()  # -180 to +180
        if ( self.turtle.physics.getSpeed() > 0.1 ):
            if (-45 <= motionAngle and motionAngle <= 45):
                self.turtle.angle = 0
            elif (45 <= motionAngle and motionAngle <= 135):
                self.turtle.angle = 90
            elif (-135 <= motionAngle and motionAngle <= -45):
                self.turtle.angle = 270
            else: 
                self.turtle.angle = 180
    
game = MapExplorer()
game.run()

# to check which parts require the most time to run, use a profiler:
# cProfile.run("game.run()")
