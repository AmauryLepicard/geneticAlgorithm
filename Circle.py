import numpy as np
import math
import Parameters

class Asteroid:
    def __init__(self, x, y, r, c, v, theta):
        self.pos = np.array((x, y))
        self.radius = r
        self.color = c
        self.mass = 100 * self.radius ** 2
        self.speed = v
        self.theta = theta

    def update(self, delta):
        self.pos[0] += self.speed * math.cos(self.theta) * delta
        self.pos[1] += self.speed * math.sin(self.theta) * delta
        self.pos = np.mod(self.pos, np.array([Parameters.SCREEN_WIDTH, Parameters.SCREEN_HEIGHT]))

