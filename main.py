import pygame

import Game
from Parameters import *

pygame.init()

# screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
area = pygame.Rect(-BORDER_SIZE, -BORDER_SIZE, SCREEN_WIDTH + 2 * BORDER_SIZE, SCREEN_HEIGHT + 2 * BORDER_SIZE)

# text
myFont = pygame.font.SysFont(None, 30)
pygame.display.set_caption("Asteroids")

mouseSprite = pygame.sprite.Sprite()

game = Game.Game(screen, area, asteroidsNumber=ASTEROID_NUMBER)

t = pygame.time.get_ticks()
while 1:
    oldT = t
    t = pygame.time.get_ticks()
    pygame.time.wait(15)
    delta = t - oldT

    # render text
    label = myFont.render(str(len(game.asteroids)), 1, (255, 255, 255))

    screen.fill((0, 0, 0))
    screen.blit(label, (0, 0))
    game.update(delta)
    pygame.display.flip()
