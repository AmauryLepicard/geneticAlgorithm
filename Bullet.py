import math
import numpy as np
import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, color, speed, theta):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        self.pos = np.array([x, y])
        self.speed = speed
        self.theta = theta

        self.color = color

        # unpowered ship image
        self.bulletImage = pygame.Surface((8, 4))
        self.bulletImage.set_colorkey((0, 0, 0))
        pygame.draw.polygon(self.bulletImage, self.color, [(0, 0), (8, 2), (0, 4)], 0)

        # generating  rect
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 8, 4)
        self.rect.center = (self.pos[0], self.pos[1])

        self.mask = pygame.mask.from_surface(self.bulletImage)

        self.image = self.bulletImage

    def update(self, delta):
        thetaVector = np.array([math.cos(self.theta), math.sin(self.theta)])

        self.pos += delta * self.speed * thetaVector
        # self.pos = np.mod(self.pos, [SCREEN_WIDTH, SCREEN_HEIGHT])

        self.image = pygame.transform.rotozoom(self.bulletImage, -self.theta * 180 / math.pi, 1.0)

        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(center=(self.pos[0], self.pos[1]))
        self.mask = pygame.mask.from_surface(self.bulletImage)
