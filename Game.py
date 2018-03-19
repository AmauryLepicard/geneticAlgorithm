import math
import random
import sys

import numpy as np
import pygame

from Asteroid import Asteroid
from Parameters import *


class Game:

    def __init__(self, screen, area, asteroidsNumber):
        self.screen = screen
        self.area = area
        self.asteroids = pygame.sprite.Group()
        self.createAsteroids(asteroidsNumber)

    def createAsteroids(self, number):
        # print("Creating", number, "asteroids")
        for i in range(number):

            # choose random color
            randColor = random.randint(150, 255)
            randColor = (randColor, randColor, randColor)

            # choose position outside of screen
            # First choose one of the 4 borders
            border = random.randint(0, 3)
            if border == 0:  # left border
                x = random.uniform(0, BORDER_SIZE)
                y = random.uniform(0, SCREEN_HEIGHT + 2 * BORDER_SIZE)
            elif border == 1:  # right border
                x = random.uniform(SCREEN_WIDTH + BORDER_SIZE, SCREEN_WIDTH + 2 * BORDER_SIZE)
                y = random.uniform(0, SCREEN_HEIGHT + 2 * BORDER_SIZE)
            elif border == 2:  # top border
                x = random.uniform(0, SCREEN_WIDTH + 2 * BORDER_SIZE)
                y = random.uniform(0, BORDER_SIZE)
            elif border == 3:  # top border
                x = random.uniform(0, SCREEN_WIDTH + 2 * BORDER_SIZE)
                y = random.uniform(SCREEN_HEIGHT + BORDER_SIZE, SCREEN_HEIGHT + 2 * BORDER_SIZE)
            else:
                # print("WAT", border)
                pass

            destX = random.uniform(BORDER_SIZE + SCREEN_WIDTH * 0.25, BORDER_SIZE + SCREEN_WIDTH * 0.75)
            destY = random.uniform(BORDER_SIZE + SCREEN_HEIGHT * 0.25, BORDER_SIZE + SCREEN_HEIGHT * 0.75)
            theta = math.atan2(destY - y, destX - x)

            c = Asteroid(x=x, y=y, radius=random.uniform(20.0, 50.0), color=randColor,
                         speed=ASTEROID_MAX_SPEED * random.uniform(0.5, 1.0), theta=theta)

            self.asteroids.add(c)

    def destroyAsteroid(self, a):
        # print("Destroying", a.name)
        self.asteroids.remove(a)
        del a

    def manageInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                #print("exiting...")  #
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for a in self.asteroids:
                    if a.radius > np.linalg.norm(a.pos - np.array(pos)):
                        if a.mass > MIN_ASTEROID_MASS:
                            self.split(a)
                        self.asteroids.remove(a)
                        del a

    def split(self, a):
        childRadius = a.radius / math.sqrt(2.0)
        theta1 = a.theta + math.pi / 8.0
        theta2 = a.theta - math.pi / 8.0
        pos1 = a.pos + childRadius * np.array([math.cos(theta1), math.sin(theta1)])
        pos2 = a.pos + childRadius * np.array([math.cos(theta2), math.sin(theta2)])
        a1 = Asteroid(pos1[0], pos1[1], childRadius, a.color, a.speed, theta1)
        a2 = Asteroid(pos2[0], pos2[1], childRadius, a.color, a.speed, theta2)
        self.asteroids.add(a1)
        self.asteroids.add(a2)
        # print("Splitting", a.name, "into", a1.name, ",", a2.name)
        self.destroyAsteroid(a)

    def update(self, delta):
        self.manageInput()

        if ENABLE_ASTEROID_COLLISION:
            for a1 in self.asteroids:
                for a2 in self.asteroids:
                    if a1 == a2:
                        break
                    if pygame.sprite.collide_mask(a1, a2) is not None:
                        a1.fixCollisionPositions(a2)
                        a1.computeCollisionSpeed(a2)
                        if a1.mass > MIN_ASTEROID_MASS:
                            self.split(a1)
                        if a2.mass > MIN_ASTEROID_MASS:
                            self.split(a2)

        for a in self.asteroids:
            if not self.area.colliderect(a):
                self.asteroids.remove(a)
                del a
                self.createAsteroids(1)

        self.asteroids.update(delta)
        self.asteroids.draw(self.screen)
