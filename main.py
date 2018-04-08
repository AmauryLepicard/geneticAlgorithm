import sys

import pygame

import AIPlayer
import GameModel
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


game = GameModel.GameModel(area, asteroidsNumber=ASTEROID_NUMBER)

player = AIPlayer.AIPlayer(game)
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            sys.exit()
        if game.isOver and (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
            game.restart()
        if game.isOver and event.type == pygame.MOUSEBUTTONDOWN:
            game.restart()

    # update gameModel
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
        # update gameModel model
        game.update(delta)
        player.update(delta)

        # draw gameModel
        game.asteroidsGroup.update(delta)
        game.asteroidsGroup.draw(screen)

        game.ship.update(delta)
        game.shipGroup.draw(screen)

        game.bulletsGroup.update(delta)
        game.bulletsGroup.draw(screen)

        # show quadrant lines#
        #        nbQuadrants = 8
        #        for i in range(nbQuadrants):
        #            angle = gameModel.ship.theta + (i+0.5)*2*math.pi/nbQuadrants
        #            delta = np.array((2000*math.cos(angle), 2000*math.sin(angle)))
        #            pygame.draw.aaline(screen, (100,100,100), gameModel.ship.pos, gameModel.ship.pos+delta)

        timeLabel = myFont30.render("Input: " + str(player.inputVector), 1, (255, 255, 255))
        screen.blit(timeLabel, (0, 70))
        timeLabel = myFont30.render("Output: " + str(player.commands), 1, (255, 255, 255))
        screen.blit(timeLabel, (0, 100))

    pygame.display.flip()
