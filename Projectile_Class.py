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
    
    
    terminalPhase = False

    # PoH and its modifiers
    POH = 0.95               # Base PoH - basically this is the chance we will hit a "normal"-sized target at point-blank range
    lifeTime = 0.0
    distanceTravelled = 0.0
    minPoH = 0.1

    def __init__ (self, ident, target, origin, totalSpeed, pos = None, name = None):
        self.ID = ident
        self.targetVessel = target
        self.originVessel = origin
        self.totalSpeed = totalSpeed
        self.name = "Projectile No. " + str(self.ID)
        self.vesselType = "missile"
        self.faction = self.originVessel.faction
        
        
        
        if not pos :
            self.pos = self.originVessel.pos
            self.originPoint = self.pos 
        

        self.takeAim()
        self.updateVelocityVector ()

    def updateTargetDistance (self):
        self.targetDistance = math.sqrt(np.dot(self.targetVessel.pos - self.pos, self.targetVessel.pos - self.pos))



    # There is a problem with this... once we reached our destination the projectile will oszilate around the destination point! We want it to keep flying!
    def updateVelocityVector (self):
        pass
        # Get the direction
        #vel = self.aimPoint - self.pos
        # Get the length of the direction vector
        #lenght = math.sqrt(np.dot(self.targetVessel.pos - self.pos, self.targetVessel.pos - self.pos))
        # Divide by lenght of direction vector (set length to one)
        #vel = vel/lenght
        # Multiply by the totalSpeed
        #self.velocity = vel * self.totalSpeed

    def update(self, dT):
        super().update(dT)      
        self.updateTargetDistance()
        self.updateDistanceTravelled()

        if self.isAlive:
            self.lifeTime = self.lifeTime + dT
            #print("Lifetime: ", + self.lifeTime)
        if not self.terminalPhase:
            #self.updateVelocityVector ()
            self.detectHit()
        if self.lifeTime > 30.0:
            self.isAlive = False

    # Since we are moving along a straight line is is very simple!
    def updateDistanceTravelled (self):
        self.distanceTravelled = np.dot(self.pos -self.originPoint, self.pos -self.originPoint)

    # We have reached the terminal phase  - let's see if we hit anything!
    def detectHit(self):
        

        if self.targetDistance < self.terminalRange:
            self.terminalPhase = True
            finalPoH = self.POH * self.targetVessel.size
            lifeTimeMod = (1/(self.lifeTime/10+1)) + self.minPoH
            finalPoH *= lifeTimeMod
            print("Lifetime: ", self.lifeTime)
            print("Lifetime modifier: ", lifeTimeMod)
            print("Final PoH is: ", finalPoH)

            if random.random() < self.POH:
                print ("Target has been hit!")
                self.isAlive = False
                self.velocity = self.velocity * 0
                self.totalSpeed = 0.0
                # For the time being everything will just die on a single hit - damage model should come later!
                self.targetVessel.isAlive = False
            else:
                print ("Target has been missed!")
            

    def detectDestinationReached(self): # What happens if we reach the destination but the target is not there anymore...
        if self.aimPoint - self.pos < self.terminalRange/10 :
            self.terminalPhase = True
            print("Aimpoint reached!")

    # this function can only be called when the missile is launched!
    def takeAim (self):
        t = 0

        #self.totalSpeed += math.sqrt(np.dot(self.originVessel.velocity, self.originVessel.velocity))

        posRel = self.pos - self.targetVessel.pos 
        velRel = self.originVessel.velocity - self.targetVessel.velocity
        #velRel =  - self.targetVessel.velocity

        a = (np.dot(velRel, velRel))-(self.totalSpeed**2)
        b = 2.0 * (np.dot(velRel,posRel))
        c = np.dot(posRel, posRel)

        disc = (b*b) - (4.0*a*c)

        print("Disc: ", disc)

        if disc < 0:
            print("Target is too fast - no point shooting!")
        else:
            t0 = (-b - math.sqrt(disc)) / (2.0*a)
            t1 = (-b + math.sqrt(disc)) / (2.0*a)

            print("t0: ", t0)
            print("t1: ", t1)

            if t0 < 0:
                t = t1
                print ("Choosing t1")
            elif t1 < 0:
                t = t0
                print ("Choosing t0")
            else:
                if t0 < t1:
                    t = t0
                    print("Choosing t0")
                else: 
                    t = t1
                    print("Choosing t1")

        shoot = velRel + (posRel / t)
        self.velocity =  shoot + self.targetVessel.velocity
        self.aimPoint = self.targetVessel.pos + self.targetVessel.velocity*t
        targetDirection = self.aimPoint-self.pos
        targetDistance = math.sqrt(np.dot(targetDirection, targetDirection))
        targetDirection = targetDirection / targetDistance #normalize the direction vector
        self.totalSpeed = targetDistance/t
        self.velocity = (targetDirection * self.totalSpeed)
        print(self.totalSpeed)
