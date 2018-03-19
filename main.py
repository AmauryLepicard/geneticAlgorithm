import pygame
import sys

import Game
from Parameters import *

pygame.init()

# screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
area = pygame.Rect(-BORDER_SIZE, -BORDER_SIZE, SCREEN_WIDTH + 2 * BORDER_SIZE, SCREEN_HEIGHT + 2 * BORDER_SIZE)

# text
myFont = pygame.font.SysFont(None, 30)
myFont2 = pygame.font.SysFont(None, 200)
pygame.display.set_caption("Asteroids")

mouseSprite = pygame.sprite.Sprite()

game = Game.Game(screen, area, asteroidsNumber=ASTEROID_NUMBER)
gameOver = False

clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            sys.exit()

    if not gameOver:
        # update game
        delta = clock.tick(60)

        # clear screen
        screen.fill((0, 0, 0))

        # render text
        asteroidsDestroyedLabel = myFont.render("Asteroids destroyed: " + str(game.score), 1, (255, 255, 255))
        screen.blit(asteroidsDestroyedLabel, (0, 0))

        timeLabel = myFont.render("Time: " + str(game.age), 1, (255, 255, 255))
        screen.blit(timeLabel, (0, 35))

        if game.update(delta) == -1:
            label = myFont2.render("GAME OVER", 1, (255, 255, 255))
            screen.blit(label, ((SCREEN_WIDTH - label.get_width()) / 2, (SCREEN_HEIGHT - label.get_height()) / 2))
            gameOver = True

        pygame.display.flip()
