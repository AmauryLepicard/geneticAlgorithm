import math
import random
from itertools import accumulate

import numpy as np
import pygame
from numpy.linalg import norm

from Parameters import *


class Asteroid(pygame.sprite.Sprite):
    nextAsteroidNumber = 0

    def __init__(self, x, y, radius, color, speed, theta):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        self.name = "a" + str(Asteroid.nextAsteroidNumber)
        Asteroid.nextAsteroidNumber += 1
        self.pos = np.array((x, y))
        self.radius = radius
        self.color = color
        self.mass = 100 * self.radius ** 2
        self.speed = speed
        self.theta = theta

        self.image = pygame.Surface((int(self.radius * 2), int(self.radius * 2)))
        self.image.set_colorkey((0, 0, 0))

        if USE_IRREGULAR_POLYGONS:
            vectorList = self.generateShape(50)
        else:
            vectorList = [(int(self.radius + self.radius * math.cos(i * 2 * math.pi / 12.0)),
                           int(self.radius + self.radius * math.sin(i * 2 * math.pi / 12.0))) for i in range(12)]

        self.rect = pygame.draw.polygon(self.image, self.color, vectorList, 5)
        self.rect.x = self.pos[0] - self.radius
        self.rect.y = self.pos[1] - self.radius

        self.mask = pygame.mask.from_surface(self.image)

    def generateShape(self, edgeNumber):
        xList = list(sorted(np.random.randint(-self.radius, self.radius, edgeNumber)))
        yList = list(sorted(np.random.randint(-self.radius, self.radius, edgeNumber)))
        xList.sort()
        yList.sort()

        xShuffled = random.sample(list(xList[1:-1]), edgeNumber - 2)
        xList1 = [xList[0]] + xShuffled[:int(len(xShuffled) / 2)] + [xList[-1]]
        xList2 = [xList[0]] + xShuffled[int(len(xShuffled) / 2):] + [xList[-1]]

        yShuffled = random.sample(list(yList[1:-1]), edgeNumber - 2)
        yList1 = [yList[0]] + yShuffled[:int(len(yShuffled) / 2)] + [yList[-1]]
        yList2 = [yList[0]] + yShuffled[int(len(yShuffled) / 2):] + [yList[-1]]

        xDeltas = [xList1[i + 1] - xList1[i] for i in range(len(xList1) - 1)] + [xList2[i] - xList2[i + 1] for i in
                                                                                 range(len(xList2) - 1)]
        yDeltas = [yList1[i + 1] - yList1[i] for i in range(len(yList1) - 1)] + [yList2[i] - yList2[i + 1] for i in
                                                                                 range(len(yList2) - 1)]
        random.shuffle(xDeltas)
        random.shuffle(yDeltas)

        vectorList = [(x, y) for x, y in zip(xDeltas, yDeltas)]
        vectorList = sorted(vectorList, key=lambda vector: -np.arctan2(vector[0], vector[1]))
        vectorList = list(accumulate(vectorList, lambda a, b: (a[0] + b[0], a[1] + b[1])))
        vectorList = [(int(x), int(y)) for x, y in vectorList]

        minX = min(v[0] for v in vectorList)
        maxX = max(v[0] for v in vectorList)
        minY = min(v[1] for v in vectorList)
        maxY = max(v[1] for v in vectorList)
        xVector = np.array([v[0] for v in vectorList])
        yVector = np.array([v[1] for v in vectorList])
        xVector = (xVector - minX) * 2 * self.radius / (maxX - minX)
        yVector = (yVector - minY) * 2 * self.radius / (maxY - minY)
        vectorList = [(int(x), int(y)) for x, y in zip(xVector, yVector)]
        return vectorList

    def update(self, delta):
        self.pos[0] += self.speed * math.cos(self.theta) * delta
        self.pos[1] += self.speed * math.sin(self.theta) * delta
        #self.pos = np.mod(self.pos, np.array([Parameters.SCREEN_WIDTH, Parameters.SCREEN_HEIGHT]))
        self.rect.x = self.pos[0] - self.radius
        self.rect.y = self.pos[1] - self.radius

    def computeCollisionSpeed(self, a2):
        # print("Collision between", self.name, "and", a2.name)
        v = self.pos - a2.pos
        # correct the distance
        v = v * (self.radius + a2.radius) / norm(v)
        v = v / norm(v)

        u = np.matmul([[0, 1], [-1, 0]], v)
        # referential change matrix
        m1 = np.array([u, v]).transpose()
        m2 = np.linalg.inv(m1)

        # Base referential speed
        v1 = np.array([[self.speed * math.cos(self.theta)], [self.speed * math.sin(self.theta)]])
        v2 = np.array([[a2.speed * math.cos(a2.theta)], [a2.speed * math.sin(a2.theta)]])

        # collision referential speed
        v1_prime = np.matmul(m2, v1)
        v2_prime = np.matmul(m2, v2)

        # update collision referential speed
        new_a1x_speed = ((self.mass - a2.mass) * v1_prime[1] + (a2.mass * 2) * v2_prime[1]) / (self.mass + a2.mass)
        new_a2x_speed = ((self.mass * 2) * v1_prime[1] + (a2.mass - self.mass) * v2_prime[1]) / (self.mass + a2.mass)

        new_v1_prime = np.array([v1_prime[0], new_a1x_speed])
        new_v2_prime = np.array([v2_prime[0], new_a2x_speed])

        # updated base referential speed
        new_v1 = np.matmul(m1, new_v1_prime)
        new_v2 = np.matmul(m1, new_v2_prime)

        # Computing asteroid speed and angle
        self.speed = norm(new_v1)
        a2.speed = norm(new_v2)

        self.theta = np.arctan2(new_v1[1], new_v1[0])
        a2.theta = np.arctan2(new_v2[1], new_v2[0])

    def fixCollisionPositions(self, a2):
        v = self.pos - a2.pos
        growthRatio = (self.radius + a2.radius) / norm(v)
        collisionPoint = a2.pos + v * (self.mass / (self.mass + a2.mass))
        new_a1_pos = collisionPoint + (self.pos - collisionPoint) * growthRatio
        new_a2_pos = collisionPoint + (a2.pos - collisionPoint) * growthRatio
        self.pos = new_a1_pos
        a2.pos = new_a2_pos

