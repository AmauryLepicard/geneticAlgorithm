import math
import random
import sys

import numpy as np
import pygame
from numpy.linalg import norm

import Parameters
from Asteroid import Asteroid

pygame.init()
screen = pygame.display.set_mode((Parameters.SCREEN_WIDTH, Parameters.SCREEN_HEIGHT))
myFont = pygame.font.SysFont(None, 15)

asteroids = pygame.sprite.Group()
for i in range(5):
    randColor = random.randint(50, 255)
    randColor = (randColor, randColor, randColor)
    c = Asteroid("a" + str(i), random.uniform(0, Parameters.SCREEN_WIDTH), random.uniform(0, Parameters.SCREEN_HEIGHT),
                 random.uniform(20.0, 50.0), randColor, random.uniform(0.0, 0.3), random.uniform(0, 2 * math.pi))

    asteroids.add(c)

# asteroids.append(Asteroid("pink", 10.0,10.0,40,(255,0,255),0.2,math.pi/4))
# asteroids.append(Asteroid("green", 10.0,400.0,40,(0,255, 0),0.2,-math.pi/3))

mouseSprite = pygame.sprite.Sprite()

t = pygame.time.get_ticks()
while 1:
    oldT = t
    t = pygame.time.get_ticks()
    delta = t-oldT
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            print("exiting...")  #
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            for a in asteroids:
                if a.radius > norm(a.pos - np.array(pos)):
                    print(a.name, "destroyed")
                    Asteroid.destroyAsteroid(a)

    for a1 in asteroids:
        for a2 in asteroids:
            if a1 == a2:
                break
            if (a1.radius + a2.radius) > norm(a1.pos - a2.pos):
                a1.fixCollisionPositions(a2)
                a1.computeCollisionSpeed(a2)
        a1.update(delta)

    asteroids.draw(screen)
    pygame.display.flip()
