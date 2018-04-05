import pygame, sys, cProfile
from pygame.locals import * # contains constants like QUIT, K_UP, etc.
from random        import * # contains randint, random function

sys.path.append("src/")

from ActionFactory import *
from Animation     import *
from Game          import *
from Group         import *
from Label         import *
from Sprite        import *
from Texture       import *

# Important: use JPG images whenever possible; PNG background/bricks cause big FPS loss
        
class RectangleDestroyer(Game):

    def create(self):
        
        self.setTitle("Rectangle Destroyer")
        self.fpsDisplay = True

        background = Sprite()
        background.setTexture( Texture.load("assets/rectangle-destroyer/background.jpg") )
        background.setPosition(400,300)
        self.group.addEntity(background)

        self.paddle = Sprite()
        self.paddle.setTexture( Texture.load("assets/rectangle-destroyer/paddle.png") )
        self.paddle.setPosition(400,550)
        self.group.addEntity(self.paddle)

        self.ball = Sprite()
        self.ball.setTexture( Texture.load("assets/rectangle-destroyer/ball.png") )
        self.ball.setPosition(400,525)
        self.ball.setPhysics(0,1000,0)
        self.group.addEntity( self.ball )

        self.wallGroup = Group()
        self.group.addEntity( self.wallGroup )
        wallSideTexture = Texture.load("assets/rectangle-destroyer/wall-side.jpg")  # 20 x 600
        wallTopTexture = Texture.load("assets/rectangle-destroyer/wall-top.jpg")    # 800 x 60
        leftWall = Sprite()
        leftWall.setTexture(wallSideTexture)
        leftWall.setPosition(10,300)
        rightWall = Sprite()
        rightWall.setTexture(wallSideTexture)
        rightWall.setPosition(790,300)
        topWall = Sprite()
        topWall.setTexture(wallTopTexture)
        topWall.setPosition(400,30)
        self.wallGroup.addEntity(leftWall)
        self.wallGroup.addEntity(rightWall)
        self.wallGroup.addEntity(topWall)

        self.brickGroup = Group()
        self.group.addEntity( self.brickGroup )

        brickTexture = Texture.load("assets/rectangle-destroyer/brick.jpg")

        for col in range(0,11):
            for row in range(0,8):
                brick = Sprite()
                brick.setTexture( brickTexture )
                brick.setPosition( 80 + 64 * col, 120 + row * 32 )
                self.brickGroup.addEntity( brick )

        self.messageLabel = Label()
        self.messageLabel.loadFont("assets/starfish-collector/OpenSans.ttf", 48)
        self.messageLabel.fontColor = (128,128,128)
        self.messageLabel.text = "click to start"
        self.messageLabel.setPosition(400, 400)
        self.messageLabel.alignment = "CENTER"
        self.group.addEntity(self.messageLabel)

        self.score = 0
        self.scoreLabel = Label()
        self.scoreLabel.loadFont("assets/starfish-collector/OpenSans.ttf", 36)
        self.scoreLabel.fontColor = (255,255,0)
        self.scoreLabel.text = "Score: " + str(self.score)
        self.scoreLabel.setPosition(400, 0)
        self.scoreLabel.alignment = "CENTER"
        self.group.addEntity(self.scoreLabel)
       

    def update(self):
        
        position = self.input.getMousePosition()
        self.paddle.x = position.x
        self.paddle.boundToScreen(800, 600)

        if (self.messageLabel.visible and self.messageLabel.text == "click to start"):
            self.ball.x = self.paddle.x
            if ( self.input.isMouseButtonDown() ):
                self.ball.physics.setSpeed(250)
                self.ball.physics.setMotionAngle(270)
                self.messageLabel.visible = False

        for wall in self.wallGroup.list():
            self.ball.bounceAgainst(wall)

        if ( self.ball.isOverlapping(self.paddle) ):
            self.ball.preventOverlap( self.paddle )
            paddlePercent = percent( self.ball.x, self.paddle.x - self.paddle.width/2, self.paddle.x + self.paddle.width/2)
            reboundAngle  = lerp( paddlePercent, 225, 315 ) + randomBetween(-2,2)
            self.ball.physics.setMotionAngle( reboundAngle )
            self.ball.physics.setSpeed( self.ball.physics.getSpeed() + 2 )
            self.score += 1

        for brick in self.brickGroup.list():
            if (self.ball.isOverlapping(brick)):
                self.ball.bounceAgainst(brick)
                brick.remove()
                self.score += 100

        self.scoreLabel.text = "Score: " + str(self.score)

        if ( (self.messageLabel.visible == False) and (self.ball.y > 700) ):
            self.ball.physics.setSpeed(0)
            self.ball.setPosition( self.paddle.x, self.paddle.y - 20 )
            self.messageLabel.visible = True
            self.messageLabel.text = "click to start"
        
        if ( self.brickGroup.count == 0 ):
            self.messageLabel.visible = True
            self.messageLabel.setPosition(400,300)
            self.messageLabel.fontColor = (0, 255, 0)
            self.messageLabel.text = "You Win!"


# helper functions

def lerp(percent, minimum, maximum):
    return minimum + percent * (maximum - minimum)

def percent(value, minimum, maximum):
    return (value - minimum) / (maximum - minimum)

def randomBetween(minimum, maximum):
    return minimum + random() * (maximum - minimum)


###### end of class
            
game = RectangleDestroyer()
#game.run()

# to check which parts require the most time to run, use a profiler:
cProfile.run("game.run()")



