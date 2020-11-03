import Vessel_Class as vc
import threading
import time

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

    def spawnVessel(self, posx, posy, name = ""):
        if name == "":
            name = "Ship No.", self.nextID
        self.vessels.append(vc.Vessel(id = self.nextID, posx = posx, posy = posy, name = name))
        self.nextID += 1

    def spawnProjectile(self, target, origin, speed, posx = None, posy = None):
        self.vessels.append(vc.Projectile(id = self.nextID, posx = posx, posy = posy, target = target, origin = origin, totalSpeed = speed))
        self.nextID += 1


    # dT neu berechnen!
    def mainLoop (self):
        told = time.time()
        while self.polling:
            
            tcurr = time.time()
            dT = tcurr - told
            #print(dT)
            if dT > self.pollingInterval:
            
                for v in self.vessels:
                    #v.xSpeed = v.xSpeed * dT
                    v.update(dT)
                print("Polling...")

                told = tcurr

    