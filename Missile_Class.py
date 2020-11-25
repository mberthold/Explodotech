import Vessel_Class

class Missile(Vessel_Class.Vessel):
    """Simple template for guided missiles"""
    max_acceleration = 0.0
    energy = 0.0

    def adjust_course (self):
        pass