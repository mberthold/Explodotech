import Vessel_Class
import math
import random
import numpy as np

# An unguided projectile
class Projectile (Vessel_Class.Vessel):
    aimPoint = None
    originPoint = None
    targetVessel = None     # make sure this is a Vessel-object!
    originVessel = None     # make sure this is a Vessel-object!
    targetDistance = -1
    terminalRange = 1.0     # At what distance do we calculate a hit?
    totalSpeed = 0.0
    lifeTime = 0.0
    distanceTravelled = 0.0
    
    terminalPhase = False

    # PoH and its modifiers
    POH = 0.5               # Probability of hit

    def __init__ (self, id, target, origin, totalSpeed, pos = None, name = None):
        self.ID = id
        self.targetVessel = target
        self.originVessel = origin
        self.totalSpeed = totalSpeed
        
        
        
        if not pos :
            self.pos = self.originVessel.pos
            self.originPoint = self.pos 
        

        self.takeAim()
        self.updateVelocityVector ()

    def updateTargetDistance (self):
        self.targetDistance = math.sqrt(np.dot(self.targetVessel.pos - self.pos, self.targetVessel.pos - self.pos))



    # There is a problem with this... once we reached our destination the projectile will oszilate around the destination point! We want it to keep flying!
    def updateVelocityVector (self):
        # Get the direction
        vel = self.targetVessel.pos - self.pos
        # Get the length of the direction vector
        lenght = math.sqrt(np.dot(self.targetVessel.pos - self.pos, self.targetVessel.pos - self.pos))
        # Divide by lenght of direction vector (set length to one)
        vel = vel/lenght
        # Multiply by the totalSpeed
        self.velocity = vel * self.totalSpeed

    def update(self, dT):
        super().update(dT)      
        self.updateTargetDistance()
        self.updateDistanceTravelled()

        if self.isAlive:
            self.lifeTime = self.lifeTime + dT
            #print("Lifetime: ", + self.lifeTime)
        if not self.terminalPhase:
            self.updateVelocityVector ()
            self.detectHit()

    # Since we are moving along a straight line is is very simple!
    def updateDistanceTravelled (self):
        self.distanceTravelled = np.dot(self.pos -self.originPoint, self.pos -self.originPoint)

    # We have reached the terminal phase  - let's see if we hit anything!
    def detectHit(self):
        if self.targetDistance < self.terminalRange:
            self.terminalPhase = True
            if random.random() < self.POH:
                print ("Target has been hit!")
                self.isAlive = False
                self.velocity = self.velocity * 0
                self.totalSpeed = 0.0
            else:
                print ("Target has been missed!")
            

    def detectDestinationReached(self): # What happens if we reach the destination but the target is not there anymore...
        if self.aimPoint - self.pos < self.terminalRange/10 :
            self.terminalPhase = True

    # this function can only be called when the missile is launched!
    def takeAim (self):
        if math.sqrt(np.dot(self.targetVessel.velocity, self.targetVessel.velocity)) == 0.0: # if our traget is not moving
            self.aimPoint = self.targetVessel.pos
        else:
            toTarget = self.targetVessel.pos - self.pos
            targetVelocity = self.targetVessel.velocity

            a = np.dot(targetVelocity, targetVelocity) - self.totalSpeed**2
            b = 2 * np.dot(targetVelocity, toTarget)
            c = np.dot(toTarget, toTarget)

            p = -b / (2*a)
            q = math.sqrt((b * b) - 4 * a * c) / (2 * a)

            t1 = p - q
            t2 = p + q
            t = None

            if t1 > t2 and t2 > 0:

                t = t2

            else:

                t = t1

            self.aimPoint = self.targetVessel.pos + self.targetVessel.velocity * t
            
         
            