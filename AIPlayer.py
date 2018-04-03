from NeuralNetwork import NeuralNetwork
import numpy as np
import math
from Parameters import *

np.set_printoptions(precision=2, suppress=True)


class AIPlayer:
    def __init__(self, game):
        self.neuralNetwork = NeuralNetwork(8, [3], 3)

        # print(self.neuralNetwork)
        # game to get data from and send input to
        self.game = game

        # keep input and output to print them on screen
        self.inputVector = np.zeros(8)
        self.commands = np.zeros(3)

    def DNA(self):
        return self.neuralNetwork.DNA()

    def update(self, delta):
        # get environment data from game
        nbQuadrants = 8  # number of quadrants in the front 180° arc
        distances = math.inf * np.ones(nbQuadrants)

        # compute referential change matrix for the ship
        rotMatrix = np.array([[math.cos(self.game.ship.theta), math.sin(self.game.ship.theta)],
                              [-math.sin(self.game.ship.theta), math.cos(self.game.ship.theta)]])

        # print("Ship angle:", self.game.ship.theta, "Rotation Matrix:", rotMatrix.flatten())
        for a in self.game.asteroidsGroup:
            # compute the asteroid coordinates in the ship's referential
            deltaPos = a.pos - self.game.ship.pos
            deltaPos1 = np.matmul(rotMatrix, deltaPos)

            # find in which quadrant is the asteroid
            relativeAngle = np.arctan2(deltaPos1[1], deltaPos1[0])
            quadrantIndex = int(round(relativeAngle / (math.pi * 2 / nbQuadrants)) % nbQuadrants)
            #           print("Angle:", relativeAngle, "Rounded:", round(relativeAngle / (math.pi * 2 / nbQuadrants)), "Quadrant:", quadrantIndex,"\n", end="", flush=True)

            # compute the distance and update NN inputs
            distance = np.linalg.norm(deltaPos1)
            # print("Asteroid", a.name ,"in quadrant ",self.quadrantIndex, "at", distance)
            distances[quadrantIndex] = min(distances[quadrantIndex], distance)

        # compute commands
        self.inputVector = 100.0 / distances
        self.commands = self.neuralNetwork.compute(self.inputVector)
        self.commands = np.clip(self.commands, -1.0, 1.0)
        # print(self.inputVector, self.commands)

        # send self.commands to game
        # rotation command
        self.game.ship.thetaSpeed = SHIP_TURN_RATE * self.commands[0]

        # acceleration command
        self.commands[1] = np.round(self.commands[1])
        self.game.ship.acceleration = max(0.0, self.commands[1]) * SHIP_ACCELERATION

        # firing command
        self.game.ship.toggleFire(self.commands[2] >= 0.0)
