import math

import numpy as np
import pygame


class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, color, speed, theta):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # position
        self.pos = np.array([x, y]).astype(float)

        #speed
        self.theta = theta
        self.speed = speed

        #acceleration
        self.thetaSpeed = 0.0
        self.acceleration = 0.0

        self.color = color

        self.size = 30
        self.unpoweredShipImage = pygame.Surface((self.size * 2, self.size + 1))
        self.unpoweredShipImage.set_colorkey((0, 0, 0))

        pygame.draw.aalines(self.unpoweredShipImage, self.color, False,
                            [(0, 0), (self.size * 2, self.size * 0.5), (0, self.size)], 1)
        pygame.draw.aalines(self.unpoweredShipImage, self.color, False,
                            [(self.size * 0.5, self.size * 0.125), (self.size * 0.5, self.size * 0.875)], 1)

        self.poweredShipImage = self.unpoweredShipImage.copy()
        pygame.draw.aalines(self.poweredShipImage, self.color, False,
                            [(0, 0), (self.size * 2, self.size * 0.5), (0, self.size)], 1)

        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size, self.size * 2)
        self.rect.center = (self.pos[0], self.pos[1])

        self.mask = pygame.mask.from_surface(self.unpoweredShipImage)
        self.image = self.unpoweredShipImage

    def update(self, delta):
        self.theta += delta * self.thetaSpeed
        self.speed += self.acceleration
        self.speed *= 0.99

        self.pos += np.array(delta * self.speed * np.array([math.cos(self.theta), math.sin(self.theta)]))

        if self.acceleration > 0.0:
            self.image = pygame.transform.rotozoom(self.unpoweredShipImage, -self.theta * 180 / math.pi, 1.0)
        else:
            self.image = pygame.transform.rotozoom(self.poweredShipImage, -self.theta * 180 / math.pi, 1.0)

        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(center=(self.pos[0], self.pos[1]))
        self.mask = pygame.mask.from_surface(self.unpoweredShipImage)
