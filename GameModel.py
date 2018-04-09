import math
import random

import numpy as np
import pygame

from Asteroid import Asteroid
from Bullet import Bullet
from Parameters import *
from Ship import Ship


class GameModel:

    def __init__(self, randomState, area, asteroidsNumber):

        random.seed(randomState)
        self.area = area

        # create asteroidsGroup
        self.asteroidNumber = asteroidsNumber
        self.asteroidsGroup = pygame.sprite.Group()
        self.createAsteroids(self.asteroidNumber)
        # print([a.pos for a in self.asteroidsGroup.sprites()[:5]])

        # create player ship
        self.ship = Ship(x=int(SCREEN_WIDTH * 0.5), y=int(SCREEN_HEIGHT * 0.5), color=(255, 255, 255), speed=0.1,
                         theta=0.0)
        self.shipGroup = pygame.sprite.GroupSingle(self.ship)

        # create bullets
        self.bulletsGroup = pygame.sprite.Group()

        self.score = 0
        self.age = 0

        self.isOver = False

    def restart(self):
        random.seed(0)

        # create asteroidsGroup
        self.asteroidsGroup = pygame.sprite.Group()
        self.createAsteroids(self.asteroidNumber)
        # print([a.pos for a in self.asteroidsGroup.sprites()[:5]])

        # create player ship
        self.ship = Ship(x=int(SCREEN_WIDTH * 0.5), y=int(SCREEN_HEIGHT * 0.5), color=(255, 255, 255), speed=0.1,
                         theta=0.0)
        self.shipGroup = pygame.sprite.GroupSingle(self.ship)

        # create bullets
        self.bulletsGroup = pygame.sprite.Group()

        self.score = 0
        self.age = 0

        self.isOver = False

    def manageInput(self):
        if not SHIP_USING_NEURAL_NETWORK:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.ship.thetaSpeed = -SHIP_TURN_RATE
            elif keys[pygame.K_RIGHT]:
                self.ship.thetaSpeed = SHIP_TURN_RATE
            else:
                self.ship.thetaSpeed = 0.0
            self.ship.acceleration = keys[pygame.K_UP] * SHIP_ACCELERATION
            self.ship.toggleFire(keys[pygame.K_SPACE])

    #        for event in pygame.event.get():
    #            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
    #                sys.exit()
    #
    #            if not SHIP_USE_MOUSE:
    #                if event.type == pygame.KEYDOWN:
    #                    if event.key == pygame.K_LEFT:
    #                        self.ship.thetaSpeed = -SHIP_TURN_RATE
    #                    if event.key == pygame.K_RIGHT:
    #                        self.ship.thetaSpeed = SHIP_TURN_RATE
    #                    if event.key == pygame.K_UP:
    #                        self.ship.acceleration = SHIP_ACCELERATION
    #                    if event.key == pygame.K_SPACE:
    #                        self.ship.toggleFire(True)
    #
    #                if event.type == pygame.KEYUP:
    #                    if event.key == pygame.K_LEFT:
    #                        self.ship.thetaSpeed = 0.0
    #                    if event.key == pygame.K_RIGHT:
    #                        self.ship.thetaSpeed = 0.0
    #                    if event.key == pygame.K_UP:
    #                        self.ship.acceleration = 0.0
    #                    if event.key == pygame.K_SPACE:
    #                        self.ship.toggleFire(False)
    #            else:
    #                if event.type == pygame.MOUSEBUTTONDOWN:
    #                    if pygame.mouse.get_pressed()[0]==1:
    #                        self.ship.toggleFire(True)
    #                    if pygame.mouse.get_pressed()[2]==1:
    #                        self.ship.acceleration = SHIP_ACCELERATION
    #                if event.type == pygame.MOUSEBUTTONUP:
    #                    if pygame.mouse.get_pressed()[0]==0:
    #                        self.ship.toggleFire(False)
    #                    if pygame.mouse.get_pressed()[2]==0:
    #                        self.ship.acceleration = 0.0
    #

    def update(self, delta, useInput=True):
        oldAge = self.age
        self.age += delta

        if useInput:
            self.manageInput()

        for a in self.asteroidsGroup:
            # check collision with another asteroid
            if ENABLE_ASTEROID_COLLISION:
                for a2 in self.asteroidsGroup:
                    if a == a2:
                        break
                    if pygame.sprite.collide_mask(a, a2) is not None:
                        a.fixCollisionPositions(a2)
                        a.computeCollisionSpeed(a2)
                        if a.mass > ASTEROID_MIN_MASS:
                            self.splitAsteroid(a)
                        else:
                            self.destroyAsteroid(a)
                        if a2.mass > ASTEROID_MIN_MASS:
                            self.splitAsteroid(a2)
                        else:
                            self.destroyAsteroid(a2)

            # check collision with player's ship
            if pygame.sprite.collide_mask(a, self.ship) is not None:
                self.isOver = True

            # check if asteroid is out of screen
            if not self.area.colliderect(a):
                self.asteroidsGroup.remove(a)
                del a
                self.createAsteroids(1)

        if self.ship.firing:
            if ((self.age - self.ship.firingStartDate) % SHIP_FIRING_RATE) < (
                    (oldAge - self.ship.firingStartDate) % SHIP_FIRING_RATE):
                startPoint = self.ship.pos + np.array(
                    [math.cos(self.ship.theta), math.sin(self.ship.theta)]) * SHIP_SIZE

                b = Bullet(startPoint[0], startPoint[1], (0, 255, 0),
                           1.0 + np.linalg.norm(self.ship.speedVector), self.ship.theta)
                self.bulletsGroup.add(b)

        for b in self.bulletsGroup:
            for a in self.asteroidsGroup:
                if pygame.sprite.collide_mask(a, b) is not None:
                    self.score += 1
                    if a.mass > ASTEROID_MIN_MASS:
                        self.splitAsteroid(a)
                    else:
                        self.destroyAsteroid(a)
                        self.createAsteroids(1)
            if not self.area.colliderect(b):
                self.bulletsGroup.remove(b)
                del b

        self.asteroidsGroup.update(delta)
        self.shipGroup.update(delta)
        self.bulletsGroup.update(delta)

    def createAsteroids(self, number):
        # print("Creating", number, "asteroidsGroup")
        for i in range(number):

            # choose random color
            randColor = random.randint(150, 255)
            randColor = (randColor, randColor, randColor)

            # choose position outside of screen
            # First choose one of the 4 borders
            border = random.randint(0, 3)
            x = -1
            y = -1
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
            self.asteroidsGroup.add(c)


    def destroyAsteroid(self, a):
        # print("Destroying", a.name)
        self.asteroidsGroup.remove(a)
        del a

    def splitAsteroid(self, a):
        childRadius = a.radius / math.sqrt(2.0)
        theta1 = a.theta + math.pi / 8.0
        theta2 = a.theta - math.pi / 8.0
        pos1 = a.pos + childRadius * np.array([math.cos(theta1), math.sin(theta1)])
        pos2 = a.pos + childRadius * np.array([math.cos(theta2), math.sin(theta2)])
        a1 = Asteroid(pos1[0], pos1[1], childRadius, a.color, a.speed, theta1)
        a2 = Asteroid(pos2[0], pos2[1], childRadius, a.color, a.speed, theta2)
        self.asteroidsGroup.add(a1)
        self.asteroidsGroup.add(a2)
        # print("Splitting", a.name, "into", a1.name, ",", a2.name)
        self.destroyAsteroid(a)
