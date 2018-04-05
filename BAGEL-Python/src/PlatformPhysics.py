from Physics    import *
from Vector2    import *

class PlatformPhysics(Physics):

    def __init__(self, accValue=100, maxSpeed=200, decValue=100, jumpSpeed=450, gravity=700, terminalVelocity=1000):
        super().__init__(accValue, maxSpeed, decValue)
        self.jumpSpeed = jumpSpeed
        self.gravity = gravity
        self.terminalVelocity = terminalVelocity
    
    ###### physics methods

    # note: Sprite instance is responsible to check
    #   if jumping is possible from current position
    def jump(self):
        
        self.velocityVector.y = -self.jumpSpeed

    def update(self, dt):

        # decrease horizontal speed (decelerate) when not accelerating
        if (self.accelerationVector.getLength() < 0.001):
            decelerationAmount = self.decelerationValue * dt
            walkDirection = 0
            if ( self.velocityVector.x > 0 ):
                walkDirection = 1
            else:
                walkDirection = -1
            walkSpeed = abs( self.velocityVector.x )

            walkSpeed -= decelerationAmount

            if (walkSpeed < 0):
                walkSpeed = 0

            self.velocityVector.x = walkSpeed * walkDirection

        # apply gravity
        self.accelerationVector.addValues(0, self.gravity)
            
        # apply acceleration to velocity
        self.velocityVector.addValues( self.accelerationVector.x * dt,
                                       self.accelerationVector.y * dt )

        # keep horizontal speed within set bounds
        if (self.velocityVector.x < -self.maximumSpeed):
            self.velocityVector.x = -self.maximumSpeed
        if (self.velocityVector.x >  self.maximumSpeed):
            self.velocityVector.x =  self.maximumSpeed

        # keep vertical speed within set bounds
        if (self.velocityVector.y < -self.terminalVelocity):
            self.velocityVector.y = -self.terminalVelocity
        if (self.velocityVector.y >  self.terminalVelocity):
            self.velocityVector.y =  self.terminalVelocity

        # apply velocity to position
        self.positionVector.addValues( self.velocityVector.x * dt,
                                       self.velocityVector.y * dt )

        # reset acceleration
        self.accelerationVector.setValues(0,0)
        
