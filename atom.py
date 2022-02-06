from math import sin, cos

class atom:
    def __init__(self, position, velocity, phase):
        self.position = position
        self.velocity = velocity
        self.phase = phase

    def step(self, step, magnitude, direction):
        if self.pair == None:
            self.velocity = [(self.velocity[0]+magnitude*sin(direction))*step, (self.velocity[1]+magnitude*cos(direction))*step]
            self.position = [self.position[0]+self.velocity[0], self.position[1]+self.velocity[1]]
    
    def bond(self, pair):
        self.pair = pair
        if pair == 0:
            self.pair = None