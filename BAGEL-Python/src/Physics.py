from Vector2    import *

class Physics(object):

    def __init__(self, accValue=100, maxSpeed=200, decValue=100):
        self.positionVector     = Vector2()
        self.velocityVector     = Vector2()
        self.accelerationVector = Vector2()
        self.accelerationValue  = accValue
        self.maximumSpeed       = maxSpeed
        self.decelerationValue  = decValue
        
    ###### basic methods
    
    ###### physics methods
    
    def getSpeed(self):
        return self.velocityVector.getLength()

    def setSpeed(self, speed):
        self.velocityVector.setLength(speed)

    def getMotionAngle(self):
        return self.velocityVector.getAngle()

    def setMotionAngle(self, angleDegrees):
        self.velocityVector.setAngle(angleDegrees)

    def bounceAgainst(self, surfaceAngleDegrees):
        relativeCollisionAngle = self.getMotionAngle() - surfaceAngleDegrees
        relativeBounceAngle = -relativeCollisionAngle
        self.setMotionAngle( relativeBounceAngle + surfaceAngleDegrees )
        
    def accelerateAtAngle(self, angleDegrees):
        v = Vector2()
        v.setLength(self.accelerationValue)
        v.setAngle(angleDegrees)
        self.accelerationVector.addVector(v)

    def update(self, dt):
        
        # apply acceleration to velocity
        self.velocityVector.addValues( self.accelerationVector.x * dt,
                                       self.accelerationVector.y * dt )

        speed = self.getSpeed()

        # decrease speed (decelerate) when not accelerating
        if (self.accelerationVector.getLength() < 0.001):
            speed -= self.decelerationValue * dt

        # keep speed within set bounds
        if (speed < 0):
            speed = 0
        if (speed > self.maximumSpeed):
            speed = self.maximumSpeed

        # update velocity
        self.setSpeed(speed)

        # apply velocity to position
        self.positionVector.addValues( self.velocityVector.x * dt,
                                       self.velocityVector.y * dt )

        # reset acceleration
        self.accelerationVector.setValues(0,0)
        
