import numpy as np

class Player:

    def __init__(self, x, y, v=1, c=0):
        self.x = x
        self.y = y
        self.c = c
        self.v = v

    def chase(self, other):
        
        if self.c ==0:

            if distance(self,other) <= self.v:
                self.x = other.x
                self.y = other.y
            else :
                noise = .1*np.random.randn(2)
                vector = np.array(direction(self,other))+noise
                self.x += self.v * vector[0]
                self.y += self.v * vector[1]

        elif self.c >0:
            self.c -=1


    def evade(self, other):
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