import Vessel_Class as vc
import threading
import time

class Game:
    vessels = []
    polling = True
    pollingInterval = 1.0
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
        self.vessels.append(vc.Vessel(id = self.nextID, posX = posx, posY = posy, name = name))
        self.nextID += 1

    # dT neu berechnen!
    def mainLoop (self):
        while self.polling:
            time.sleep(self.pollingInterval)
            print(time.time_ns())
            
            for v in self.vessels:
                v.xSpeed = v.xSpeed * self.pollingInterval
                v.updatePosition()
            print("Polling...")

    