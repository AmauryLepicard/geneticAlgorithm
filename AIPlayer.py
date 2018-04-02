from NeuralNetwork import NeuralNetwork
import numpy as np
import math

def relu(x):
    return max(0.0, x)

class AIPlayer:
    def __init__(self, game):
        self.nn = NeuralNetwork(12, (6, 6), 3, relu)

        # game to get data from and send input to
        self.game = game

    def DNA(self):
        return self.nn.DNA()

    def update(self, delta):
        # get environment data from game
        nbQuadrants = 16 # number of quadrants in the front 180° arc
        distances = -1 * np.ones(nbQuadrants)

        #compute referential change matrix for the ship
        shipAngle = math.atan2(self.game.ship.speedVector[1], self.game.ship.speedVector[0])
        rotMatrix = np.array([[math.cos(shipAngle), -math.sin(shipAngle)], [math.sin(shipAngle), math.cos(shipAngle)]])

        for a in self.game.asteroidsGroup:
            # compute the asteroid coordinates in the ship's referential
            deltaPos = a.pos - self.game.ship.pos
            deltaPos1 = np.matmul(rotMatrix, deltaPos)

            # find in which quadrant is the asteroid
            angle = np.arctan2(deltaPos1[1], deltaPos1[0])
            quadrantIndex = int(angle % (math.pi * 2 / nbQuadrants))

            #compute the distance and update NN inputs
            distance = np.linalg.norm(deltaPos1)
            distances[quadrantIndex] = min(distances[quadrantIndex], distance)

        print(distances)

        # compute commands


        # send commands to game


