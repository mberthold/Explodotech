# Import pyhton stuff
import threading
import time
import os
import tkinter as tk
import numpy as np


# Import my own stuff
import Vessel_Class
import Game_Class

space = Game_Class.Game()
running = True

# Initialize
def Initialize():
    print ("Initializing... \n\r")
    global space
    global updateThread
    space.spawnVessel(np.array([5.0 , 0.0]), "Rocinante")
    print ("Ship spawned... \n\r")
    space.spawnVessel(np.array([0.0 , 0.0]),  "Borg Cube")
    space.vessels[0].velocity[0] = 0.5
    print ("Missile spawned... \n\r")
    space.t1.start()
    print ("Space loop started... \n\r")
    updateThread.start() 



# GUI functions
def guiQuit():
    global running
    
    space.polling = False
    running = False
    root.destroy()
    print("GTFO!")

def btnLaunch_Event():
    global space
    print("Launchbutton pressed!")
    space.spawnProjectile(target = space.vessels[0], origin = space.vessels[1], speed = 1.0) #  target, origin, speed, posx = None, posy = None)    


def updateGUI():
    global running
    while running:
        try:
            lblShipX['text'] = round(space.vessels[0].pos[0], 2)
            lblShipY['text'] = round(space.vessels[0].pos[1], 2)
            if len(space.vessels) > 2:
                lblMissileX['text'] = round(space.vessels[2].pos[0], 2)
                lblMissileY['text'] = round(space.vessels[2].pos[1], 2)
                lblMissileSpeed['text'] = space.vessels[2].totalSpeed 
                lblMissileDistance['text'] = round(space.vessels[2].targetDistance, 2)
            time.sleep(0.1)
        except:
            print("I take exception to this!")
    print("Stopping GUI-Update...")

updateThread = threading.Thread(target = updateGUI)
   

# DEFINING GUI Elements

HEIGHT = 500
WIDTH = 500

root = tk.Tk()

canvas = tk.Canvas(root, height = HEIGHT, width = WIDTH)
canvas.pack()

frame = tk.Frame(root, bg = '#98adb9')
frame.place(relx = 0.05, rely = 0.05, relwidth = 0.9, relheight = 0.9)

btnLaunch = tk.Button(frame, text = "Launch Missile!", command = lambda: btnLaunch_Event())
btnQuit = tk.Button(frame, text = "Quit", command = guiQuit)

lblTitle = tk.Label(frame, text = "Explodotech Missile Calculator")

lblPosMissile = tk.Label(frame, text = "Missile Position:")
lblMissileX = tk.Label(frame)
lblMissileY = tk.Label(frame)

lblSpeed = tk.Label(frame, text = "Missile speed:")
lblMissileSpeed = tk.Label(frame)

lblDistance = tk.Label(frame, text = "Distance from target:")
lblMissileDistance = tk.Label(frame)

lblTime = tk.Label(frame, text = "Time:")
lblMissileTime = tk.Label(frame)

lblHit = tk.Label(frame, text = "Hit?")
lblMissileHit = tk.Label(frame)

lblPosShip = tk.Label(frame, text = "Ship Position:")
lblShipX = tk.Label(frame)
lblShipY = tk.Label(frame)

lblTitle.grid(row = 0, column = 3)
lblPosMissile.grid(row = 1, column = 0)
lblMissileX.grid(row = 2, column = 0)
lblMissileY.grid(row = 2, column = 1)
lblSpeed.grid(row = 3, column = 0)
lblMissileSpeed.grid(row = 4, column = 0)
lblDistance.grid(row = 5, column = 0)
lblMissileDistance.grid(row = 6, column = 0)
lblTime.grid(row = 7, column = 0)
lblMissileTime.grid(row = 8, column = 0)
lblHit.grid(row = 9, column = 0)
lblMissileHit.grid(row = 9, column = 1)
lblPosShip.grid(row = 1, column = 3)
lblShipX.grid(row = 2, column = 3)
lblShipY.grid(row = 2, column = 4)
btnLaunch.grid(row = 10, column = 1)
btnQuit.grid(row = 10, column = 3)



Initialize()

root.mainloop()




#clear = lambda: os.system('cls')

#clear()