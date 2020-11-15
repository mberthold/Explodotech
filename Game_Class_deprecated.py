import Vessel_Class as vc
import Projectile_Class as pc
import threading
import time
import numpy as np

class Game:
    vessels = {}
    polling = True
    pollingInterval = 0.1
    nextID = 0
    

    def __init__(self, active = False):
        self.t1 = threading.Thread(target = self.mainLoop, args = [])
        print ("Armageddon")

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

        self.vessels[self.nextID] = vc.Vessel(id = self.nextID, pos = pos, name = name)
        print(self.vessels)
        self.nextID += 1



    def spawnProjectile(self, target, origin, speed, pos = None):
        self.vessels[self.nextID] = pc.Projectile(id = self.nextID, pos = pos, target = target, origin = origin, totalSpeed = speed)
        self.nextID += 1

    def deleteVessel (self, id):
        self.vessels.pop(id)

   
    def mainLoop (self):
        t = time.time()
        
        while self.polling:
            graveyard = []  # collect the IDs of all vessels that have died this cycle in order to delete them
            t += self.pollingInterval

            for ID in self.vessels: # update all the vessels
                v = self.vessels.get(ID)
                if v.isAlive:
                    v.update(self.pollingInterval)
                else:
                    graveyard.append(ID)

            for v in graveyard: # delete alle the dead vessels!
                self.vessels.pop(v)
            #print("Polling...")

            time.sleep(max(0, t-time.time()))

        print("Shutting down mainLoop...")

    