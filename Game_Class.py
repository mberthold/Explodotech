import Vessel_Class as vc
import Projectile_Class as pc
import threading
import time
import numpy as np

class Game:
    vessels = []
    polling = True
    pollingInterval = 0.1
    nextID = 0
    

    def __init__(self, active = False):
        self.t1 = threading.Thread(target = self.mainLoop, args = [])
        

    def startPolling (self):
        self.polling = True

    def stopPolling (self):
        self.polling = False

    def togglePolling (self):
        if self.polling :
            self.polling = False
        else :
            self.polling = True
        print ("self.polling set to: ", self.polling)

    def spawnVessel(self, pos, name = ""):
        if name == "":
            name = "Ship No.", self.nextID
        self.vessels.append(vc.Vessel(id = self.nextID, pos = pos, name = name))
        self.nextID += 1


    def spawnProjectile(self, target, origin, speed, pos = None):
        self.vessels.append(pc.Projectile(id = self.nextID, pos = pos, target = target, origin = origin, totalSpeed = speed))
        self.nextID += 1


   
    def mainLoop (self):
        told = time.time()
        while self.polling:
            
            tcurr = time.time()     # calculate dT
            dT = tcurr - told
            
            if dT > self.pollingInterval:
            
                for v in self.vessels:
                    #v.xSpeed = v.xSpeed * dT
                    if v.isAlive:
                        v.update(dT)
                #print("Polling...")

                told = tcurr
        print("Shutting down...")

    