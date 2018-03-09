import pygame
import sys
import random
import time
import math
import Parameters

from Circle import Asteroid

pygame.init()
screen = pygame.display.set_mode((Parameters.SCREEN_WIDTH, Parameters.SCREEN_HEIGHT))
myFont = pygame.font.SysFont(None, 15)

asteroids = []
for i in range(20):
    randColor = (random.randint(200,255), random.randint(200,255), random.randint(200,255))
    c = Asteroid(random.uniform(0, Parameters.SCREEN_WIDTH), random.uniform(0, Parameters.SCREEN_HEIGHT), random.uniform(20, 50), randColor, 100, random.uniform(0, 2*math.pi))
    asteroids.append(c)

t = time.clock()
while 1:
    oldT = t
    t = time.clock()
    delta = t-oldT
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_a):
            print("exiting...")
            sys.exit()

    for a in asteroids:
        a.update(delta)
        pygame.draw.circle(screen, a.color, a.pos.astype(int), int(a.radius))

    for i in range(len(asteroids)):
        for j in range(i+1, len(asteroids)):
            a1 = asteroids[i]
            a2 = asteroids[j]
            if a1.radius+a2.radius < math.sqrt((a1.pos[0]-a2.pos[0])**2+(a1.pos[1]-a2.pos[1])**2):
                print("Collision")

    pygame.display.flip()
