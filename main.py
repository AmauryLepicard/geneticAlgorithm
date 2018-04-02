import pygame
import sys

import Game
import AIPlayer
from Parameters import *

pygame.init()

# screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
area = pygame.Rect(-BORDER_SIZE, -BORDER_SIZE, SCREEN_WIDTH + 2 * BORDER_SIZE, SCREEN_HEIGHT + 2 * BORDER_SIZE)

# text
myFont30 = pygame.font.SysFont(None, 30)
myFont200 = pygame.font.SysFont(None, 200)
myFont100 = pygame.font.SysFont(None, 100)
pygame.display.set_caption("Asteroids")

mouseSprite = pygame.sprite.Sprite()

#game = Game.Game(screen, area, asteroidsNumber=ASTEROID_NUMBER)
def restartGame():
    global game
    game = Game.Game(screen, area, asteroidsNumber=ASTEROID_NUMBER)
restartGame()

player = AIPlayer.AIPlayer(game)
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            sys.exit()
        if game.isOver and (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
            restartGame()
        if game.isOver and event.type == pygame.MOUSEBUTTONDOWN:
            restartGame()

    # update game
    delta = clock.tick(60)

    # clear screen
    screen.fill((0, 0, 0))

    # render text
    asteroidsDestroyedLabel = myFont30.render("Asteroids destroyed: " + str(game.score), 1, (255, 255, 255))
    screen.blit(asteroidsDestroyedLabel, (0, 0))

    timeLabel = myFont30.render("Time: " + str(game.age), 1, (255, 255, 255))
    screen.blit(timeLabel, (0, 35))

    if game.isOver:
        label = myFont200.render("GAME OVER", 1, (255, 255, 255))
        screen.blit(label, ((SCREEN_WIDTH - label.get_width()) / 2, (SCREEN_HEIGHT - label.get_height()) / 2))
        label2 = myFont100.render("Press Enter to restart, Echap to quit", 1, (255, 255, 255))
        screen.blit(label2, ((SCREEN_WIDTH - label2.get_width()) / 2, 100 + (SCREEN_HEIGHT - label2.get_height()) / 2))
        gameOver = True

    if not game.isOver:
        game.update(delta)
        player.update(delta)

    pygame.display.flip()
