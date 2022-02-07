class atom:
    def __init__(self, position, velocity, phase):
        self.position = position
        self.velocity = velocity
        self.phase = phase
        self.pair = None

    def step(self, step, magnitude):
        if self.pair == None:
            k = 1/10 # force constant
            self.velocity = [self.velocity[0]+(magnitude[0]*k),self.velocity[1]+(magnitude[1]*k)]
            self.position = [self.position[0]+self.velocity[0], self.position[1]+self.velocity[1]]
    
    def bond(self, pair): #create a bond with another atom
        self.pair = pair
        if pair == 0:
            self.pair = None
            
    def flip(self, direction):
        if direction[0]:
            self.velocity[0] = -self.velocity[0]
        if direction[1]:
            self.velocity[1] = -self.velocity[1]