import threading
import math

# The idea is that each vessel will manage its own movement in a seperate thread...
# Let's hope this does not overtax the system... ;)
class Vessel:
    # A very simple missile - maybe even the prototype for all missiles.. who knows..
    iD = "None"
    name = "New Ship"
    posX = 0.0
    posY = 0.0
    
    xSpeed = 0.0 # Units per second
    ySpeed = 0.0
    
    
    isAlive = True



    def __init__ (self, id, posx, posy, name):
        self.ID = id
        self.posX = posx
        self.posY = posy

    def getPosition (self):
        return (self.posX, self.posY)

    def setSpeed(self, xspeed, yspeed):
        print ("Setting Speed to    :   ", xspeed)
        self.xSpeed = xspeed
        self.ySpeed = yspeed
        
        
    # only for debugging purposes
    def stopMoving(self):
        self.xSpeed = 0.0

    def updatePosition(self, dT):
        self.posX = (self.xSpeed * dT) + self.posX   # Calculate new x-Position
        self.posY = (self.ySpeed * dT) + self.posY   # Calculate new y-Position

    def update(self, dT):
        self.updatePosition(dT)


# An unguided projectile
class Projectile (Vessel):
    destX = None
    destY = None
    targetVessel = None     # make sure this is a Vessel-object!
    originVessel = None     # make sure this is a Vessel-object!
    targetDistance = -1


    def __init__ (self, id, target, origin, totalSpeed, posx = None, posy = None, name = None):
        self.ID = id
        self.destX = target.posX
        self.destY = target.posY
        self.targetVessel = target
        self.originVessel = origin
        self.totalSpeed = totalSpeed
        
        if not posx :
            self.posX = self.originVessel.posX
        if not posy :
            self.posY = self.originVessel.posY

        self.updateSpeed

    def updateTargetDistance (self):
        self.targetDistance = math.sqrt((self.posX - self.targetVessel.posX)**2 + (self.posY - self.targetVessel.posY)**2)



    # There is a problem with this... once we reached our destination the projectile will oszilate around the destination point! We want it to keep flying!
    def updateSpeed(self):
        # Get the direction
        self.xSpeed = self.destX - self.posX
        self.ySpeed = self.destY - self.posY
        # Get the length of the direction vector
        lenght = math.sqrt(self.xSpeed**2+self.ySpeed**2)
        # Divide by lenght of direction vector (set length to one)
        self.xSpeed = self.xSpeed/lenght
        self.ySpeed = self.ySpeed/lenght
        # Multiply by the totalSpeed
        self.xSpeed = self.xSpeed*self.totalSpeed
        self.ySpeed = self.ySpeed*self.totalSpeed

    def update(self, dT):
        super().update(dT)
        self.updateSpeed()
        self.updateTargetDistance()

    


