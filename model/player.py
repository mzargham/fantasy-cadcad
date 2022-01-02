import numpy as np

class Player:

    def __init__(self, x, y, v=0, a=.5, c=0, r=.1, vmax=1):
        self.x = x # x position
        self.y = y # y position
        self.c = c # countdown to chase
        self.v = v # speed
        self.a = a # acceleration
        self.r = r # reach
        self.vmax = vmax
    
    def accel(self):
        self.v += self.a

        if self.v > self.vmax:
            self.v = self.vmax 


    def chase(self, other):
        
        if self.c ==0:

            self.accel()

            if distance(self,other) <= self.v:
                self.x = other.x
                self.y = other.y
            else :
                noise = .1*np.random.randn(2)
                vector = np.array(direction(self,other))+noise
                self.x += self.v * vector[0]
                self.y += self.v * vector[1]

        elif self.c >0:
            self.v = 0
            self.c -=1


    def evade(self, other):

            self.accel()

            noise = .1*np.random.randn(2)
            vector = np.array(direction(self,other))+noise
            self.x -= self.v * vector[0]
            self.y -= self.v * vector[1]


def distance(player1, player2):

    return np.sqrt((player1.x-player2.x)**2 + (player1.y - player2.y)**2 )

def direction(player1, player2):

    dist = distance(player1,player2)

    if dist > .01:
        dx = player2.x-player1.x
        dy = player2.y-player1.y
        return (dx/dist, dy/dist)

    else:
        dx = np.random.randn()
        dy = np.random.randn()
        return (dx, dy)