import math
import random

import numpy as np
import pygame.sprite
from numpy.linalg import norm

import Parameters


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, name, x, y, r, c, v, theta):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        self.name = name
        self.pos = np.array((x, y))
        self.radius = r
        self.color = c
        self.mass = 100 * self.radius ** 2
        self.speed = v
        self.theta = theta

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.image.load('Asteroid.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(self.radius * 2), int(self.radius * 2)))

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0] - self.radius
        self.rect.y = self.pos[1] - self.radius

    def generateShape(self, edgeNumber):
        xList = np.random.uniform(-self.radius, self.radius, edgeNumber)
        yList = np.random.uniform(-self.radius, self.radius, edgeNumber)
        xList.sort()
        yList.sort()
        xShuffled = random.sample(xList[1:-1], edgeNumber - 2)
        xList1 = xList[0]
        xList1.append(xShuffled[:len(xShuffled) / 2])
        xList1.append(xList[-1])
        xList2 = xList[0]
        xList2.append(xShuffled[len(xShuffled) / 2:])
        xList2.append(xList[-1])
        yShuffled = random.sample(xList[1:-1], edgeNumber - 2)
        yList1 = yList[0]
        yList1.append(yShuffled[:len(yShuffled) / 2])
        yList1.append(yList[-1])
        yList2 = xList[0]
        yList2.append(yShuffled[len(yShuffled) / 2:])
        yList2.append(yList[-1])



    def update(self, delta):
        self.pos[0] += self.speed * math.cos(self.theta) * delta
        self.pos[1] += self.speed * math.sin(self.theta) * delta
        self.pos = np.mod(self.pos, np.array([Parameters.SCREEN_WIDTH, Parameters.SCREEN_HEIGHT]))
        self.rect.x = self.pos[0] - self.radius
        self.rect.y = self.pos[1] - self.radius

    def computeCollisionSpeed(self, a2):
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

    def split(self):
        print("Splitting")

        childRadius = self.radius / math.sqrt(2.0)
        theta1 = self.theta + math.pi / 8.0
        theta2 = self.theta - math.pi / 8.0
        pos1 = self.pos + childRadius * np.array([math.cos(theta1), math.sin(theta1)])
        pos2 = self.pos + childRadius * np.array([math.cos(theta2), math.sin(theta2)])
        c1 = Asteroid(self.name + "1", pos1[0], pos1[1], childRadius, self.color, self.speed, theta1)
        c2 = Asteroid(self.name + "2", pos2[0], pos2[1], childRadius, self.color, self.speed, theta2)
        return c1, c2
