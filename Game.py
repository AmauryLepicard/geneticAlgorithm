import math
import numpy as np
import pygame
import random
import sys

import Parameters
from Asteroid import Asteroid


class Game:

    def __init__(self, screen, area, asteroidsNumber):
        self.screen = screen
        self.area = area
        self.asteroids = pygame.sprite.Group()
        self.createAsteroids(asteroidsNumber)

    def createAsteroids(self, number):
        for i in range(number):
            randColor = random.randint(150, 255)
            randColor = (randColor, randColor, randColor)
            c = Asteroid(name="a" + str(i), x=random.uniform(10, Parameters.SCREEN_WIDTH - 10),
                         y=random.uniform(10, Parameters.SCREEN_HEIGHT - 10),
                         r=50.0, c=randColor, v=random.uniform(0.0, 0.3), theta=random.uniform(0, 2 * math.pi))

            self.asteroids.add(c)
        # self.asteroids.append(Asteroid("pink", 10.0,10.0,40,(255,0,255),0.2,math.pi/4))
        # self.asteroids.append(Asteroid("green", 10.0,400.0,40,(0,255, 0),0.2,-math.pi/3))

    def manageInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                print("exiting...")  #
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for a in self.asteroids:
                    if a.radius > np.linalg.norm(a.pos - np.array(pos)):
                        if a.mass > Parameters.MIN_ASTEROID_MASS:
                            c1, c2 = a.split()
                            self.asteroids.add(c1)
                            self.asteroids.add(c2)
                        self.asteroids.remove(a)
                        del a

    def mainLoop(self):
        t = pygame.time.get_ticks()
        while 1:
            oldT = t
            t = pygame.time.get_ticks()
            delta = t - oldT
            self.screen.fill((0, 0, 0))
            self.manageInput()

            for a1 in self.asteroids:
                for a2 in self.asteroids:
                    if a1 == a2:
                        break
                    if pygame.sprite.collide_mask(a1, a2) is not None:
                        a1.fixCollisionPositions(a2)
                        a1.computeCollisionSpeed(a2)

            for a in self.asteroids:
                if not self.area.colliderect(a):
                    print("Asteroid", a.name, "(", a.pos[0], ",", a.pos[1], ") outside of area, detroy it!")
                    self.asteroids.remove(a)
                    del a

            self.asteroids.update(delta)
            self.asteroids.draw(self.screen)
            pygame.display.flip()
