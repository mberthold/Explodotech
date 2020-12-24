'''
The idea here is to make a very simple class that represents an engery event.
If such an event actually shows up as a "blip" on the scope of a ship depends on whether the ship has
sensors that can actually detect the event.

These events can be instantaneous flashes (like muzzlefire) or could can have a lifetime. 
Later on I would like to add graphs so one can analyze the signals received by the sensors. 

In terms of direction there should be three options:
omni-directional
conic
bi-conic

can we get a system that allows us the get the relative strength of a signal without having to 
calculate the distance for each ship?
'''
class Blip ():
    strength = 0
    lifetme = 0
    spectrum = "None"
    direction = "omni" 
    