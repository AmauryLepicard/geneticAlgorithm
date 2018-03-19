import math

import numpy as np
import pygame

from Parameters import *


class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, color, speed, theta):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # position
        self.pos = np.array([x, y]).astype(float)

        #speed
        self.theta = theta
        self.speedVector = np.array([speed * math.cos(self.theta), speed * math.sin(self.theta)])

        #acceleration
        self.thetaSpeed = 0.0
        self.acceleration = 0.0

        self.color = color

        self.firing = False

        # unpowered ship image
        self.unpoweredShipImage = pygame.Surface((SHIP_SIZE * 2, SHIP_SIZE + 1))
        self.unpoweredShipImage.set_colorkey((0, 0, 0))
        pygame.draw.aalines(self.unpoweredShipImage, self.color, False,
                            [(0, 0), (SHIP_SIZE * 2, SHIP_SIZE * 0.5), (0, SHIP_SIZE)], 1)
        pygame.draw.aalines(self.unpoweredShipImage, self.color, False,
                            [(SHIP_SIZE * 0.5, SHIP_SIZE * 0.125), (SHIP_SIZE * 0.5, SHIP_SIZE * 0.875)], 1)

        # powered ship image
        self.poweredShipImage = self.unpoweredShipImage.copy()
        pygame.draw.aalines(self.poweredShipImage, (255, 0, 0), False,
                            [(SHIP_SIZE * 0.5, SHIP_SIZE * 0.25), (0, SHIP_SIZE * 0.5),
                             (SHIP_SIZE * 0.5, SHIP_SIZE * 0.75)], 1)

        # generating  rect
        self.rect = pygame.Rect(self.pos[0], self.pos[1], SHIP_SIZE, SHIP_SIZE * 2)
        self.rect.center = (self.pos[0], self.pos[1])

        self.mask = pygame.mask.from_surface(self.unpoweredShipImage)

        self.image = self.unpoweredShipImage

    def update(self, delta):

        self.theta += delta * self.thetaSpeed
        thetaVector = np.array([math.cos(self.theta), math.sin(self.theta)])

        self.speedVector += delta * self.acceleration * thetaVector
        self.speedVector *= SHIP_DRAG_COEFF

        self.pos += delta * self.speedVector
        self.pos = np.mod(self.pos, [SCREEN_WIDTH, SCREEN_HEIGHT])

        if self.acceleration > 0.0:
            self.image = pygame.transform.rotozoom(self.poweredShipImage, -self.theta * 180 / math.pi, 1.0)
        else:
            self.image = pygame.transform.rotozoom(self.unpoweredShipImage, -self.theta * 180 / math.pi, 1.0)

        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(center=(self.pos[0], self.pos[1]))
        self.mask = pygame.mask.from_surface(self.unpoweredShipImage)
