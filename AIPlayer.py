from NeuralNetwork import NeuralNetwork
import numpy as np
import math
from Parameters import *
import pygame

def relu(x):
    return max(0.0, x)

class AIPlayer:
    def __init__(self, game):
        self.nn = NeuralNetwork(8, (6, 6), 3, relu)

        # game to get data from and send input to
        self.game = game
        self.commands = np.zeros(3)

    def DNA(self):
        return self.nn.DNA()

    def update(self, delta):
        # get environment data from game
        nbQuadrants = 8 # number of quadrants in the front 180° arc
        distances = math.inf * np.ones(nbQuadrants)

        #compute referential change matrix for the ship
        rotMatrix = np.array([[math.cos(self.game.ship.theta), math.sin(self.game.ship.theta)], [-math.sin(self.game.ship.theta), math.cos(self.game.ship.theta)]])

        #print("Ship angle:", self.game.ship.theta, "Rotation Matrix:", rotMatrix.flatten())
        for a in self.game.asteroidsGroup:
            # compute the asteroid coordinates in the ship's referential
            deltaPos = a.pos - self.game.ship.pos
            deltaPos1 = np.matmul(rotMatrix, deltaPos)

            # find in which quadrant is the asteroid
            relativeAngle = np.arctan2(deltaPos1[1], deltaPos1[0])
            quadrantIndex = int(round(relativeAngle / (math.pi * 2 / nbQuadrants)) % nbQuadrants)
#           print("Angle:", relativeAngle, "Rounded:", round(relativeAngle / (math.pi * 2 / nbQuadrants)), "Quadrant:", quadrantIndex,"\n", end="", flush=True)

            #compute the distance and update NN inputs
            distance = np.linalg.norm(deltaPos1)
            #print("Asteroid", a.name ,"in quadrant ",self.quadrantIndex, "at", distance)
            distances[quadrantIndex] = min(distances[quadrantIndex], distance)

        # compute commands
        danger = 10.0 / distances
        self.commands = np.clip(self.nn.compute(danger), -1.0, 1.0)
        self.commands[1] = np.round(self.commands[1])

        # send self.commands to game
        if self.commands[0] > 0.0:
            self.game.ship.thetaSpeed =-SHIP_TURN_RATE * self.commands[0]
        elif self.commands[0] < 0.0:
            self.game.ship.thetaSpeed = SHIP_TURN_RATE * self.commands[0]
        else:
            self.game.ship.thetaSpeed = 0.0
        self.game.ship.acceleration = self.commands[1] * SHIP_ACCELERATION
        self.game.ship.toggleFire(self.commands[2] >= 1.0)

