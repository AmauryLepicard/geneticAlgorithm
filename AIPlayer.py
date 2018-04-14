import math

import numpy as np

from NeuralNetwork import NeuralNetwork
from Parameters import *

np.set_printoptions(precision=2, suppress=True)


class AIPlayer:
    def __init__(self, gameModel, name):
        self.neuralNetwork = NeuralNetwork(16, [4, 4], 3)

        # print(self.neuralNetwork)
        # gameModel to get data from and send input to
        self.gameModel = gameModel

        # keep input and output to print them on screen
        self.inputVector = np.zeros(8)
        self.commands = np.zeros(3)
        self.name = name

    def DNA(self):
        return self.neuralNetwork.DNA()

    def setFromDNA(self, dna):
        self.neuralNetwork.setFromDNA(dna)

    def update(self, delta):
        # get environment data from gameModel
        nbQuadrants = 8  # number of quadrants in the front 180° arc
        distances = math.inf * np.ones(nbQuadrants)
        relativeSpeeds = np.zeros(nbQuadrants)

        # compute referential change matrix for the ship
        rotMatrix = np.array([[math.cos(self.gameModel.ship.theta), math.sin(self.gameModel.ship.theta)],
                              [-math.sin(self.gameModel.ship.theta), math.cos(self.gameModel.ship.theta)]])

        # print("Ship angle:", self.gameModel.ship.theta, "Rotation Matrix:", rotMatrix.flatten())
        for a in self.gameModel.asteroidsGroup:
            # compute the asteroid coordinates in the ship's referential
            deltaPos = a.pos - self.gameModel.ship.pos
            deltaPos1 = np.matmul(rotMatrix, deltaPos)

            # find in which quadrant is the asteroid
            relativeAngle = np.arctan2(deltaPos1[1], deltaPos1[0])
            quadrantIndex = int(round(relativeAngle / (math.pi * 2 / nbQuadrants)) % nbQuadrants)
            # print("Angle:", relativeAngle, "Rounded:", round(relativeAngle / (math.pi * 2 / nbQuadrants)), "Quadrant:", quadrantIndex,"\n", end="", flush=True)

            # compute the distance and update NN inputs
            distance = max(1.0, np.linalg.norm(deltaPos1) - a.radius - SHIP_SIZE)
            # print("Asteroid", a.name ,"in quadrant ",self.quadrantIndex, "at", distance)
            distances[quadrantIndex] = min(distances[quadrantIndex], distance)

            # compute the speed
            nextRelativePos = a.pos + delta * a.speed * np.array(
                [math.cos(a.theta), math.sin(a.theta)]) - self.gameModel.ship.pos
            relativeSpeed = distance - np.linalg.norm(nextRelativePos)
            if relativeSpeed > 0.0:
                # the asteroid is getting closer
                relativeSpeeds[quadrantIndex] = max(relativeSpeeds[quadrantIndex], relativeSpeed)

        # compute commands
        distances = 100.0 / (distances + 100.0)
        relativeSpeeds = relativeSpeeds / ASTEROID_MAX_SPEED
        self.inputVector = np.concatenate([distances, relativeSpeeds])
        self.commands = self.neuralNetwork.compute(self.inputVector)
        self.commands = np.clip(self.commands, -1.0, 1.0)
        # print(self.inputVector, self.commands)

        # send self.commands to gameModel
        # rotation command
        self.gameModel.ship.thetaSpeed = SHIP_TURN_RATE * self.commands[0]

        # acceleration command
        self.commands[1] = np.round(self.commands[1])
        self.gameModel.ship.acceleration = ((self.commands[1] + 1.0) / 2.0) * SHIP_ACCELERATION

        # firing command
        self.gameModel.ship.toggleFire(self.commands[2] >= 0.0)
